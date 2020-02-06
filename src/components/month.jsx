import React from 'react';
import Post from './post';
import axios from 'axios';
import moment from 'moment';
import lodash from 'lodash';
import { SITE_TITLE } from '../config';
import PostContainer from './post_container';

class Month extends React.Component {
  state = {
    rawPosts: []
  }

  componentDidMount() {
    let { year, month } = this.props.match.params

    document.title = SITE_TITLE

      axios.get(`/api/${year}/${month}`)
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

export default Month;
