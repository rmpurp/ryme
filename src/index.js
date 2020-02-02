import React from 'react';
import ReactDOM from 'react-dom';
import Post from './components/post';

const Index = () => {
  return <Post title="HI" date="2020-01-01" content = "HELLO WORLD"/>
};

ReactDOM.render(<Index />, document.getElementById('root'));

