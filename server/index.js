import express, { Router } from 'express';
import { join } from 'path';
import { getYearMonthPayload, getSpecificMarkdownFile, getYearMonthWithPosts, getRecentPostsPayload } from './get_posts';
import { requiresAuth } from './auth';
import { CACHE_PURGE_INTERVAL, DAYS_ON_FRONT_PAGE } from './server_config';
import { sendCachedJSON } from './cache';

const app = express();

const apiRouter = express.Router()

const port = process.env.PORT || 3000;
const DIST_DIR = join(__dirname, '../dist');
const POST_DIR = join(__dirname, '../posts');
const MEDIA_DIR = join(__dirname, '../media');

// Caching
let responseCache = new Map()
const clearCache = () => { responseCache = new Map() }
setInterval(clearCache, CACHE_PURGE_INTERVAL);

// API calls
apiRouter.post('/clear-cache', requiresAuth, (req, res) => {
  clearCache();
  res.send("Cache cleared.")
})

apiRouter.get('/:year/:month', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getYearMonthPayload(
    POST_DIR,
    req.params.year,
    req.params.month))
});

apiRouter.get('/:year/:month/:day/:title', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getSpecificMarkdownFile(
    POST_DIR,
    req.params.year,
    req.params.month,
    req.params.day,
    req.params.title
  ));
})

apiRouter.get('/archive', (req, res) => {
  sendCachedJSON(responseCache, req, res, () => getYearMonthWithPosts(POST_DIR));
})

apiRouter.get('/latest', (req, res) => {
  sendCachedJSON(responseCache, req, res,
    () => getRecentPostsPayload(POST_DIR, DAYS_ON_FRONT_PAGE));
});

apiRouter.use( (req, res) => res.status(404).send("OOF! You've been 404'd."));

app.use('/api', apiRouter);


app.get("/admin", [requiresAuth], (req, res) => {
  res.statusCode = 403;
  res.end();
});

let mediaRouter = express.Router({strict: true})

// Static resources
mediaRouter.use('/', express.static(MEDIA_DIR));
mediaRouter.use( (_, res) => res.status(404).send("OOF! You've been 404'd."));

app.use('/media', mediaRouter);

app.use('/archives', express.static(DIST_DIR));
app.use('/:year/:month', express.static(DIST_DIR));
app.use('/:year/:month/:day/:title', express.static(DIST_DIR));
app.use('/', express.static(DIST_DIR));

// app.use('/admin', express.static(DIST_DIR));

app.use(function (req, res) {
  res.status(404).send("OOF! You've been 404'd.");
});

app.listen(port, function () {
  console.log('App listening on port: ' + port);
});
