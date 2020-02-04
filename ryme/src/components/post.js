import React from 'react';
import PropTypes from 'prop-types'
import ReactMarkdown from 'react-markdown'

class Post extends React.Component {

  static propTypes = {
    title: PropTypes.string,
    date: PropTypes.object,
    content: PropTypes.string,
  };

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <article className="ryme-post">
        <div className="ryme-title">
          {this.props.title}
        </div>
        <div className="ryme-date">
          {this.props.date.format('MMMM Do, YYYY')}
        </div>
        <ReactMarkdown source={this.props.content}/>
      </article>
    );
  }
}

export default Post;
