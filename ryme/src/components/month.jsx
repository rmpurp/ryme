import React from 'react';
import Post from './post';
import axios from 'axios';
import moment from 'moment';

const sortByKey = (array, key) => {
  return array.sort(function(a, b) {
      var x = a[key]; var y = b[key];
      return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  });
}

const parseData = rawPostContent => {
    let re = /^@@Title=(.+)$\n+^@@Date=(.+)$\n+^([\d\D]+)/m
    let matches = rawPostContent.match(re);
    if (matches) {
      return {
        title: matches[1],
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

    let {year, month} = this.props.match.params

    axios.get(`/api/${year}/${month}`)
      .then((response) => {
        let posts = sortByKey(response.data.posts.map(parseData), "date")
        this.setState({posts: posts})
      })
  }


  render() {
    console.log("RENDERING")
    console.log(this.state.posts)

    let posts = this.state.posts.map(post => {
      return <Post {...post} key={post.date}/>
    });

    return (
      <div className="ryme-articles">
      {posts}
      </div>
    ) 
  }
}

export default Month;
