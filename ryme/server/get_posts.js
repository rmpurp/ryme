const glob = require('glob')
const util = require('util')
const path = require('path'); // NEW
const fs = require('fs')


const globPromise = util.promisify(glob)
const readFilePromise = util.promisify(fs.readFile)

exports.getSpecificMarkdownFile = (directory, yearString, monthString, dayString, title) => {
  let Glob = glob.Glob
  let options = { cwd: directory }
  let path = path.join(yearString, monthString, dayString, `${title}.md`)
}

exports.getYearMonthPayload = async (
  directory,
  yearString,
  monthString,
  cache) => {
  // cacheContent = cache.get(i)
  // let key = {year: {yearString}, month: {monthString}} 

  let searchPath = path.join(yearString, monthString, "*", "*.md");

  let files = await globPromise(searchPath, { cwd: directory });
  return await Promise.all(
    files.map(fp => {
      return readFilePromise(path.join(directory, fp), { encoding: "utf8" })
   }));
}
