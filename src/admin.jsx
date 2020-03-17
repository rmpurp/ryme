import React from 'react';
import ReactDOM from 'react-dom';
import { DeletePostList } from './admin_components/delete_post_list';
import { PostCreator } from './admin_components/post_creator';

// eslint-disable-next-line no-unused-vars
import _ from './style.css';

const Index = () => {
  return (
    <>
      <DeletePostList/>
      <PostCreator/>
    </>
  );
};

ReactDOM.render(<Index />, document.getElementById('root'));
