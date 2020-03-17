import express, { Router } from 'express';
import { join } from 'path';
import { 
  getYearMonthPayload,
  getSpecificMarkdownFile,
  getYearMonthWithPosts,
  getRecentPostsPayload,
  getPosts } from './get_posts';
import { requiresAuth } from './auth';
import { CACHE_PURGE_INTERVAL, DAYS_ON_FRONT_PAGE } from './server_config';
import { sendCachedJSON } from './cache';
import { Post } from './records';

import { deletePost, createPost } from './post_management';

const app = express();
const port = process.env.PORT || 3000;
const DIST_DIR = join(__dirname, '../dist');
const POST_DIR = join(__dirname, '../posts');
const MEDIA_DIR = join(__dirname, '../media');

// Caching
let responseCache = new Map();
const clearCache = () => {
  responseCache = new Map();
};

setInterval(clearCache, CACHE_PURGE_INTERVAL);


// API calls
const apiRouter = Router({ strict: true });

apiRouter.get('/:year/:month', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getYearMonthPayload(
    POST_DIR,
    req.params.year,
    req.params.month));
});

apiRouter.get('/:year/:month/:day/:title', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getSpecificMarkdownFile(
    POST_DIR,
    req.params.year,
    req.params.month,
    req.params.day,
    req.params.title,
  ));
});

apiRouter.get('/archive', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getYearMonthWithPosts(POST_DIR));
});

apiRouter.get('/latest', (req, res) => {
  sendCachedJSON(responseCache, req, res,
    () => getRecentPostsPayload(POST_DIR, DAYS_ON_FRONT_PAGE));
});

apiRouter.use( (req, res) => res.status(404).send('OOF! You\'ve been 404\'d.'));
app.use('/api', apiRouter);

// Admin API calls
const adminApiRouter = Router({ strict: true });
adminApiRouter.use(express.json());

adminApiRouter.get('/all-posts', async (req, res) => {
  res.json({ content: await getPosts(POST_DIR) });
});

adminApiRouter.post('/create-post', (req, res) => {
  let post = Post(req.body);
  let postContent = req.body.content;
  console.log(postContent);
  let creationStatus = createPost(POST_DIR, post, postContent);
  clearCache();
  res.sendStatus(creationStatus ? 200 : 400);
});


adminApiRouter.post('/delete-post', async (req, res) => {
  let post = Post(req.body);
  // 
  let deleteStatus = await deletePost(POST_DIR, post);

  clearCache();
  res.sendStatus(deleteStatus ? 200 : 400);
});

adminApiRouter.use( (req, res) => res.status(404).send('OOF! You\'ve ben 404\'d.'));

app.use('/admin-api', requiresAuth);
app.use('/admin-api', adminApiRouter);


// Admin panel
app.get('/admin', [requiresAuth], (req, res) => {
  res.sendFile(join(DIST_DIR, 'admin.html'));

});

// Media resources
const mediaRouter = Router({ strict: true });
mediaRouter.use('/', express.static(MEDIA_DIR));
mediaRouter.use( (_, res) => res.status(404).send('OOF! You\'ve been 404\'d.'));


app.use(express.static(DIST_DIR));

app.use('/media', mediaRouter);

app.get(['/', '/*'], function(req, res) {
  res.sendFile(join(DIST_DIR, 'index.html'));
});

app.use(function(req, res) {
  res.status(404).send('OOF! You\'ve been 404\'d.');
});

app.listen(port, '0.0.0.0', function() {
  console.log('App listening on port: ' + port);
});
