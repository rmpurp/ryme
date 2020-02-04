const express = require('express');
const path = require('path'); // NEW
const postIO = require('./get_posts')
const app = express();

const port = process.env.PORT || 3000;
const DIST_DIR = path.join(__dirname, '../dist');

const HTML_FILE = path.join(DIST_DIR, 'index.html');
const POST_DIR = path.join(__dirname, '../posts')

var router = express.Router();


app.get('/api/:year/:month', (req, res) => {
    console.log("HERE")
    postIO.getYearMonthPayload(POST_DIR, req.params.year, req.params.month, null)
        .then(posts => {
            res.json({ posts: posts })
        })
});

app.get('/api/:year/:month/:day/:title', (req, res) => {
    console.log(req.params)
    postIO.getSpecificMarkdownFile(POST_DIR, req.params.year, req.params.month, req.params.day, req.params.title)
        .then(post => {
            res.json({ post: post })
        })
})

app.get('/api/latest', (req, res) => {
    postIO.getYearMonthWithPosts(POST_DIR).then(yearMonthMap => {
        console.log(yearMonthMap)
        latestYear = [...yearMonthMap.keys()].sort().pop()
        latestMonth = [...(yearMonthMap.get(latestYear))].sort().pop()
        console.log(latestYear, latestMonth)
        postIO.getYearMonthPayload(POST_DIR, latestYear, latestMonth, null)
            .then(posts => {
                console.log(posts);
                res.json({ posts: posts })
            })
    })
})

app.use('/', express.static(DIST_DIR));
app.use('/:year/:month', express.static(DIST_DIR));
app.use('/:year/:month/:day/:title', express.static(DIST_DIR));

app.get("/", (req, res) => {
    res.sendFile(HTML_FILE);
})

app.get("/:year/:month", (req, res) => {
    res.sendFile(HTML_FILE);
})


app.get("/:year/:month/:day/:title", (req, res) => {
    res.sendFile(HTML_FILE);
})

app.listen(port, function() {
    console.log('App listening on port: ' + port);
});