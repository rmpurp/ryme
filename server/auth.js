import auth from 'basic-auth';
import compare from 'tsscmp';
import bcrypt from 'bcryptjs';
import { USERNAME, PASSWORD_HASH } from './server_config';

/**
 * Express middleware for requiring authentication using Basic Auth
 * @param {} req the Express request
 * @param {*} res the Express response
 * @param {*} next next middleware to call
 */
export const requiresAuth = (req, res, next) => {
  let credentials = auth(req);

  if (!credentials || !check(credentials.name, credentials.pass)) {
    res.statusCode = 401;
    res.setHeader('WWW-Authenticate', 'Basic realm="Admin panel"');
    res.end('Access denied');
  } else {
    next();
  }
};

/**
 * 
 * @param {string} name - the username to be checked
 * @param {string} pass - the password to be checked
 */
export const check = (name, pass) => {
  var valid = true;

  valid = compare(name, USERNAME) && valid;
  valid = bcrypt.compareSync(pass, PASSWORD_HASH) && valid;

  return valid;
};
