import glob from 'glob';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs';
import lodash from 'lodash';
import { Month, Day, Post } from './records';
import { OrderedSet } from 'immutable';

const globPromise = promisify(glob);
const readFilePromise = promisify(fs.readFile);

export const getSpecificMarkdownFile = async (directory, yearString, monthString, dayString, title) => {
  let fp = path.join(directory, yearString, monthString, dayString, `${title}.md`);
  return {
    slug: path.parse(fp).name,
    rawPostContent: await readFilePromise(fp, { encoding: 'utf8' })
  };
};

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

export const getYearMonthPayload = async (
  directory,
  yearString,
  monthString) => {

  let searchPath = path.join(yearString, monthString, '*', '*.md');
  return getPayloadWithSearchPath(directory, searchPath);
};


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


export const getYearMonthWithPosts = async (directory) => {
  let posts = await getPosts(directory);
  return posts.map(post => Month(post)); // Filters out duplicates
};

export const getRecentPostsPayload = async (directory, numDays) => {
  let posts = await getPosts(directory);
  let promises = posts
    .map(post => Day(post))
    .take(numDays)
    .map(day => path.join(day.year, day.month, day.day, '*.md'))
    .map(searchPath => getPayloadWithSearchPath(directory, searchPath));
  posts = await Promise.all(promises);
  return  posts.flat();
};

