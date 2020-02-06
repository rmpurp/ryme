const glob = require('glob')
const util = require('util')
const path = require('path'); // NEW
const fs = require('fs');
const lodash = require('lodash');

const globPromise = util.promisify(glob);
const readFilePromise = util.promisify(fs.readFile);

exports.getSpecificMarkdownFile = async(directory, yearString, monthString, dayString, title) => {
    let Glob = glob.Glob;
    let options = { cwd: directory };
    let fp = path.join(directory, yearString, monthString, dayString, `${title}.md`);
    return {
        slug: path.parse(fp).name,
        rawPostContent: await readFilePromise(fp, { encoding: "utf8" })
    }
}

exports.getYearMonthPayload = async(
    directory,
    yearString,
    monthString) => {
    // cacheContent = cache.get(i)
    // let key = {year: {yearString}, month: {monthString}} 

    let searchPath = path.join(yearString, monthString, "*", "*.md");

    let files = await globPromise(searchPath, { cwd: directory });
    return await Promise.all(
        files.map(async fp => {
            const contents = await readFilePromise(path.join(directory, fp), { encoding: "utf8" });
            return { slug: path.parse(fp).name, rawPostContent: contents };
        }));
}

exports.getYearMonthWithPosts = async(directory) => {
    let searchPath = path.join("*", "*", "*", "*.md");
    let yearToMonth = new Map()
    let entries = []
    let files = await globPromise(searchPath, { cwd: directory });
    files.forEach(fp => {
        let [year, month, day, name] = fp.split(path.sep);
        entries.push({year, month});
    });

    return lodash.sortBy(entries, ["year", "month"])
}