import React from 'react';
import Post from './post';
import moment from 'moment';
import { sortBy } from 'lodash';
import PropTypes from 'prop-types';

const parseData = ({ slug, rawPostContent }) => {
  const re = /^@@Title=(.+)$\n+^@@Date=(.+)$\n+^([\d\D]+)/m;
  const matches = rawPostContent.match(re);
  if (matches) {
    return {
      title: matches[1],
      slug: slug,
      date: moment(matches[2]),
      content: matches[3],
    };
  }
};

class PostContainer extends React.Component {
  static propTypes = {
    rawPosts: PropTypes.array,
    setTitle: PropTypes.bool,
  };

  render() {
    const sortedPosts = sortBy(this.props.rawPosts.map(parseData), 'date')
      .reverse();

    if (this.props.setTitle && sortedPosts.length == 1) {
      document.title = sortedPosts[0].title;
    }

    const posts = sortedPosts.map((post) => {
      return <Post {...post} key={post.date} />;
    });

    return (
      <div className="ryme-articles">
        {posts ? posts : <p>Loading...</p>}
      </div>
    );
  }
}

export default PostContainer;
