import React from 'react';
import Post from './post';
import axios from 'axios';
import moment from 'moment';

const sortByKey = (array, key) => {
  return array.sort(function (a, b) {
    var x = a[key]; var y = b[key];
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  });
}

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

class Month extends React.Component {
  state = {
    posts: []
  }

  componentDidMount() {
    console.log("PROPS:", this.props)

    let { year, month } = this.props.match.params

    if (year && month) {
    axios.get(`/api/${year}/${month}`)
      .then((response) => {
        let posts = sortByKey(response.data.posts.map(parseData), "date")
        this.setState({ posts: posts })
      })
    } else {
    axios.get(`/api/latest`)
      .then((response) => {
        console.log(response.data);
        let posts = sortByKey(response.data.posts.map(parseData), "date")
        this.setState({ posts: posts })
      })
    }
  }


  render() {
    let posts = this.state.posts.map(post => {
      return <Post {...post} key={post.date} />
    });

    return (
      <div className="ryme-articles">
        {posts}
      </div>
    )
  }
}

export default Month;
