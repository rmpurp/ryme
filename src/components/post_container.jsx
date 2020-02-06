import React from 'react';
import Post from './post';
import moment from 'moment';
import { sortBy } from 'lodash';

const parseData = ({ slug, rawPostContent }) => {
  let re = /^@@Title=(.+)$\n+^@@Date=(.+)$\n+^([\d\D]+)/m
  let matches = rawPostContent.match(re);
  if (matches) {
    return {
      title: matches[1],
      slug: slug,
      date: moment(matches[2]),
      content: matches[3],
    }
  }
}

class PostContainer extends React.Component {

  render() {
    let sortedPosts = sortBy(this.props.rawPosts.map(parseData), "date").reverse()

    if (this.props.setTitle && sortedPosts.length == 1) {
      document.title = sortedPosts[0].title
    }

    let posts = sortedPosts.map(post => {
      return <Post {...post} key={post.date} />
    });

    return (
      <div className="ryme-articles">
        {posts ? posts : <Text>Loading...</Text>}
      </div>
    )
  }
}

export default PostContainer;
