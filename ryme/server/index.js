const express = require('express');
const path = require('path'); // NEW
const postIO = require('./get_posts')
const app = express();

const port = process.env.PORT || 3000;
const DIST_DIR = path.join(__dirname, '../dist');

const HTML_FILE = path.join(DIST_DIR, 'index.html');
const POST_DIR = path.join(__dirname, '../posts')

let yearMonthToPayloadCache = new Map()

app.get('/api/:year/:month', (req, res) => {
  postIO.getYearMonthPayload(POST_DIR, req.params.year, req.params.month, null)
  .then ( posts => {
    res.send({posts: posts})
  })
});

app.use('/', express.static(DIST_DIR));
app.use('/:year/:month', express.static(DIST_DIR));
app.use('/:year/:month/:day/:title', express.static(DIST_DIR));


app.get("/:year/:month/:day/:title", (req, res) => {
  res.sendFile(HTML_FILE);
})
app.get("/:year/:month", (req, res) => {
  res.sendFile(HTML_FILE);
})

app.get("/", (req, res) => {
  res.sendFile(HTML_FILE);
})

app.listen(port, function () {
  console.log('App listening on port: ' + port);
});
