import React from 'react';
import Post from './post';
import axios from 'axios';
import moment from 'moment';
import lodash from 'lodash';
import { SITE_TITLE } from '../config';
import PostContainer from './post_container';


class RecentPosts extends React.Component {
  state = {
    rawPosts: []
  }

  componentDidMount() {
    document.title = SITE_TITLE

    axios.get(`/api/latest`)
      .then((response) => {
        this.setState({ rawPosts: response.data.content })
      })
  }


  render() {
    return (
      <PostContainer rawPosts={this.state.rawPosts} />
    )
  }
}

export default RecentPosts;
