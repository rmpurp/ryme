import React from 'react';

class Post extends React.Component {
  render() {
    return (
      <div className="ryme-post">
        <div className="ryme-title">
          {this.props.title}
        </div>
        <div className="ryme-date">
          {this.props.date}
        </div>
        <div className="ryme-content">
          {this.props.content}
        </div>
      </div>
    );
  }
}

export default Post;