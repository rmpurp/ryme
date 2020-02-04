import React from 'react';
import ReactDOM from 'react-dom';
import Month from './components/month';
import MastHead from './components/masthead';
import SinglePost from './components/single_post';
import _ from './style.css';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";

const Index = () => {

  return (
    <>

      <Router>
        <MastHead />

        <Switch>
          <Route exact path="/" component={Month} />
          <Route exact path="/:year/:month" component={Month} />
          <Route exact path="/:year/:month/:day/:title" component={SinglePost} />
        </Switch>
      </Router>
    </>
  )
};

ReactDOM.render(<Index />, document.getElementById('root'));

