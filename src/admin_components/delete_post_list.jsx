import React from 'react';
import axios from 'axios';
import lodash from 'lodash';

/**
 * A list of all the posts with the ability to delete them.
 */
export class DeletePostList extends React.Component {

  state = {
    posts: []
  };

  componentDidMount() {
    this.fetchPosts();
  }

  /**
   * Fetches posts from the admin API.
   */
  fetchPosts() {
    axios.get('/admin-api/all-posts').then(response => {
      let posts = response.data.content;
      this.setState({
        posts: lodash.sortBy(posts, ['year', 'month', 'day', 'slug'])
      });

    });
  }

  /**
   * Makes an API call to remove the post.
   * @param {*} post 
   */
  removePost(post) {
    const shouldDelete = window.confirm('Really delete?');
    if (shouldDelete) {
      axios.post('/admin-api/delete-post', post).then(() => {
        this.fetchPosts();
      });
    }
  }

  render() {
    let rendered = this.state.posts.map(post => {
      const { year, month, day, slug } = post;
      return (
        <li key={JSON.stringify(post)}>
          <button onClick={() => this.removePost(post)}>Delete {year}/{month}/{day}/{slug}</button>
        </li>
      );
    });

    return (
      <ul>
        {rendered}
      </ul>
    );
  }
}