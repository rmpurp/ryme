import express, { Router } from 'express';
import { join } from 'path';
import { getYearMonthPayload, getSpecificMarkdownFile, getYearMonthWithPosts } from './get_posts';
const app = express();

const port = process.env.PORT || 3000;
const DIST_DIR = join(__dirname, '../dist');

const HTML_FILE = join(DIST_DIR, 'index.html');
const POST_DIR = join(__dirname, '../posts')

var router = Router();

let responseCache = new Map()

const makeCacheKey = (req) => {
  return [req.path].concat(Object.keys(req.params).sort()
    .map(key => `${key}=${req.params[key]}`)
  ).join("$$RYME_SEPARATOR$$")
}

const probeCacheElseFetch = (req, onMiss, finalAction) => {
  let key = req.path;
  let cachedValue;
  if (cachedValue = responseCache.get(key)) {
    console.log(`Cache hit with key ${key}`)
    finalAction(cachedValue);
  } else {
    console.log(`Cache miss with key ${key}`)
    onMiss().then(fetchedValue => {
      responseCache.set(key, fetchedValue);
      finalAction(fetchedValue);
    })
  }
};

const sendCachedJSON = (req, res, onMiss) => {
  probeCacheElseFetch(req, onMiss, (fetchedValue) => {
    res.json({ content: fetchedValue });
  });
};

const clearCache = () => { responseCache = new Map() }

// TODO: Make main site render past 10 posts instead of most recent month

app.get('/api/:year/:month', (req, res) => {
  sendCachedJSON(req, res, () => getYearMonthPayload(
    POST_DIR,
    req.params.year,
    req.params.month))
});

app.get('/api/:year/:month/:day/:title', (req, res) => {
  sendCachedJSON(req, res, () => getSpecificMarkdownFile(
    POST_DIR,
    req.params.year,
    req.params.month,
    req.params.day,
    req.params.title
  ));
})

app.get('/api/archive', (req, res) => {
  sendCachedJSON(req, res, () => getYearMonthWithPosts(POST_DIR));
})

app.get('/api/latest', (req, res) => {
  getYearMonthWithPosts(POST_DIR).then(yearMonthMap => {
    latestYear = [...yearMonthMap.keys()].sort().pop()
    latestMonth = [...(yearMonthMap.get(latestYear))].sort().pop()
    getYearMonthPayload(POST_DIR, latestYear, latestMonth, null)
      .then(posts => {
        res.json({ posts: posts })
      })
  })
})

app.use('/', express.static(DIST_DIR));
app.use('/:year/:month', express.static(DIST_DIR));
app.use('/:year/:month/:day/:title', express.static(DIST_DIR));

app.get("/", (req, res) => {
  res.sendFile(HTML_FILE);
});

app.get("/archives", (req, res) => {
  res.sendFile(HTML_FILE);
});

app.get("/:year/:month", (req, res) => {
  res.sendFile(HTML_FILE);
});

app.get("/:year/:month/:day/:title", (req, res) => {
  res.sendFile(HTML_FILE);
});

app.use(function (req, res) {
  res.status(404).send("ERROR 404: There's nothing here. Sorry.");
});

app.listen(port, function () {
  console.log('App listening on port: ' + port);
});