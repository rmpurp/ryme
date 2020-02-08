import React from 'react';
import PropTypes from 'prop-types';
import ReactMarkdown from 'react-markdown';
import PostFooter from './post_footer';
import { PERMALINK_SYMBOL } from '../config';

import {
  Link,
} from 'react-router-dom';

/**
 * Component that renders posts from Markdown into HTML.
 */
class Post extends React.Component {
  static propTypes = {
    title: PropTypes.string,
    date: PropTypes.object,
    slug: PropTypes.string,
    content: PropTypes.string,
  };

  constructor(props) {
    super(props);
  }

  render() {
    const year = this.props.date.format('YYYY');
    const month = this.props.date.format('MM');
    const day = this.props.date.format('DD');
    const permalink = `/${year}/${month}/${day}/${this.props.slug}`;
    return (
      <article className="ryme-post">
        <header>
          <div className="ryme-title">
            {this.props.title}
          </div>
          <p>

            <span className="ryme-date">
              {this.props.date.format('MMMM Do, YYYY')}
            </span>
            <Link to={permalink} className="ryme-permalink">
              {PERMALINK_SYMBOL}
            </Link>
          </p>
          <div className="ryme-date">
          </div>
        </header>
        <ReactMarkdown className="ryme-content" source={this.props.content} />
        <PostFooter />
      </article>
    );
  }
}

export default Post;
