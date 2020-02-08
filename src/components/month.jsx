import React from 'react';
import axios from 'axios';
import { SITE_TITLE } from '../config';
import PostContainer from './post_container';
import PropTypes from 'prop-types';

class Month extends React.Component {
  state = {
    rawPosts: []
  }

  static propTypes = {
    match: PropTypes.object,
  };

  componentDidMount() {
    let { year, month } = this.props.match.params;

    document.title = SITE_TITLE;

    axios.get(`/api/${year}/${month}`)
      .then((response) => {
        this.setState({ rawPosts: response.data.content });
      });
  }


  render() {
    return (
      <PostContainer rawPosts={this.state.rawPosts} />
    );
  }
}

export default Month;
