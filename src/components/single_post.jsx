import React from 'react';
import axios from 'axios';
import PostContainer from './post_container';

class SinglePost extends React.Component {
  state = {
    rawPosts: [] 
  }

  componentDidMount() {
    let { year, month, day, title } = this.props.match.params

    axios.get(`/api/${year}/${month}/${day}/${title}`)
      .then((response) => {
        // let post = parseData(response.data.content)
        // document.title = post.title
        this.setState({ rawPosts: [response.data.content] })
      })
  }


  render() {

    return (
        <PostContainer rawPosts={this.state.rawPosts} setTitle />
    )
  }
}

export default SinglePost;
