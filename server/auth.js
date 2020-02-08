import auth from 'basic-auth';
import compare from 'tsscmp';
import bcrypt from 'bcrypt';
import { USERNAME, PASSWORD_HASH } from './server_config';

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

export const check = (name, pass) => {
  var valid = true;

  valid = compare(name, USERNAME) && valid;
  valid = bcrypt.compareSync(pass, PASSWORD_HASH) && valid;

  return valid;
};
