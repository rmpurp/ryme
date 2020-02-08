import React from 'react';
import axios from 'axios';
import PostContainer from './post_container';
import PropTypes from 'prop-types';

class SinglePost extends React.Component {
  state = {
    rawPosts: [] 
  }


  static propTypes = {
    match: PropTypes.object
  };


  componentDidMount() {
    let { year, month, day, title } = this.props.match.params;

    axios.get(`/api/${year}/${month}/${day}/${title}`)
      .then((response) => {
        this.setState({ rawPosts: [response.data.content] });
      });
  }


  render() {

    return (
      <PostContainer rawPosts={this.state.rawPosts} setTitle />
    );
  }
}

export default SinglePost;
