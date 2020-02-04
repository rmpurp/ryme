import React from 'react';
import ReactDOM from 'react-dom';
import Month from './components/month'
import _ from './style.css';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";

const Index = () => {

  return (
    <Router>
      <Switch>
        <Route exact path="/" component={Month}>
        </Route>
        <Route exact path="/:year/:month" component={Month}>

        </Route>
      </Switch>
    </Router>
  )
};

ReactDOM.render(<Index />, document.getElementById('root'));

