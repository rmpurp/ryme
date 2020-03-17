import { promises } from 'fs';
import { join } from 'path';

/**
 * Asynchronously deletes a post.
 * @param {string} directory - the directory the posts are written to
 * @param {Post} post - The post. An object with the post's year, month, day, and slug
 * @returns {boolean} - true if successful, false else
 */
export const deletePost = async (directory, post) => {
  const fp = join(directory, post.year, post.month, post.day, `${post.slug}.md`);
  try {
    await promises.unlink(fp);
    // TODO: clean up empty directories
    console.log('Deleted post ${post.slug}');
    return true;
  } catch(err) {
    // File does not exist.
    console.log(err);
    return false;
  }
};

/**
 * Asynchronously creates a post, overwriting it if it already exists.
 * @param {string} directory - the directory the posts are writen to
 * @param {Post} post - the post. Contains the post's year, month, day, and slug
 * @param {string} postContents - the contents of the post
 * @returns {boolean} - true if successful, false else
 */
export const createPost = async (directory, post, postContents) => {
  const postDir = join(directory, post.year, post.month, post.day);
  const fp = join(postDir, `${post.slug}.md`);
  
  await promises.mkdir(postDir, { recursive: true });

  try {
    console.log(`Created post ${post.slug} at ${postDir}`);
    await promises.writeFile(fp, postContents);
  } catch(err) {
    console.log(err);
  }
};
