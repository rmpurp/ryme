import React from 'react';
import Post from './post';
import axios from 'axios';
import moment from 'moment';

const parseData = ({ slug, rawPostContent }) => {
  console.log("SDFLDSKJFLDKSJ");
  console.log(`SLUG: ${slug}`);
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
class SinglePost extends React.Component {
  state = {
    post: undefined
  }

  componentDidMount() {
    let { year, month, day, title } = this.props.match.params
    console.log(year, month, day, title);

    axios.get(`/api/${year}/${month}/${day}/${title}`)
      .then((response) => {
        console.log(response);
        let post = parseData(response.data.post)
        this.setState({ post: post })
      })
  }


  render() {
    let contents = <p>Loading...</p>
    if (this.state.post) {
      contents = <Post {...this.state.post} />
    }

    return (
      <div className="ryme-articles">
        {contents}
      </div>
    )
  }
}

export default SinglePost;
