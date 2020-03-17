import glob from 'glob';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';
import lodash from 'lodash';
import { Month, Day, Post } from './records';
import { OrderedSet } from 'immutable';

const globPromise = promisify(glob);
const readFilePromise = promisify(fs.readFile);
// TODO: switch to promise.readFile

/**
 * 
 * @param {string} directory - the post directory
 * @param {string} yearString - 4-digit year string
 * @param {string} monthString - zero-padded month string
 * @param {string} dayString - zero-padded day string
 * @param {*} title - The slug of the post, to which ".md" will be added
 */
export const getSpecificMarkdownFile = async (directory, yearString, monthString, dayString, title) => {
  let fp = path.join(directory, yearString, monthString, dayString, `${title}.md`);
  return {
    slug: path.parse(fp).name,
    rawPostContent: await readFilePromise(fp, { encoding: 'utf8' })
  };
};

/**
 * Get the API payload with posts matching the search path
 * @param {string} directory the post directory
 * @param {string} searchPath the glob search path to match files with
 */
const getPayloadWithSearchPath = async (
  directory,
  searchPath) => {
  let files = await globPromise(searchPath, { cwd: directory });
  return await Promise.all(
    files.map(async fp => {
      const contents = await readFilePromise(path.join(directory, fp), { encoding: 'utf8' });
      return { slug: path.parse(fp).name, rawPostContent: contents };
    }));
};

/**
 * Get the API payload for posts during the year and month
 * @param {string} directory - the post directory
 * @param {string} yearString - 4-digit year string
 * @param {string} monthString - zero-padded month string
 */
export const getYearMonthPayload = async (
  directory,
  yearString,
  monthString) => {

  let searchPath = path.join(yearString, monthString, '*', '*.md');
  return getPayloadWithSearchPath(directory, searchPath);
};

/**
 * Get all the posts in the directory
 * @param {*} directory the root post directory
 */
export const getPosts = async (directory) => {
  let searchPath = path.join('*', '*', '*', '*.md');
  let files = await globPromise(searchPath, { cwd: directory });
  let entries = [];
  files.forEach(fp => {
    let [year, month, day, name] = fp.split(path.sep);
    let slug = name.replace(/\.md$/, '');
    entries.push(Post({ year, month, day, slug }));
  });

  return OrderedSet(lodash.sortBy(entries, ['year', 'month', 'day']));
};

/**
 * Get all months (object containing year with month) during which there is
 * at least one post.
 * @param {string} directory - the post directory
 */
export const getYearMonthWithPosts = async (directory) => {
  let posts = await getPosts(directory);
  return posts.map(post => Month(post)); // Filters out duplicates
};

/**
 * Get API payload containing recent posts.
 * @param {string} directory - the post directory
 * @param {number} count - the number of posts to fetch
 */
export const getRecentPostsPayload = async (directory, count) => {
  let posts = await getPosts(directory);
  let promises = posts
    .map(post => Day(post))
    .take(count)
    .map(day => path.join(day.year, day.month, day.day, '*.md'))
    .map(searchPath => getPayloadWithSearchPath(directory, searchPath));
  posts = await Promise.all(promises);
  return  posts.flat();
};

