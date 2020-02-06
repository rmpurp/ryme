import React from 'react';
import ReactDOM from 'react-dom';
import Month from './components/month';
import MastHead from './components/masthead';
import SinglePost from './components/single_post';
import SiteFooter from './components/site_footer';
import Archives from './components/archive';
import RecentPosts from './components/recent_posts'
import _ from './style.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

const Index = () => {

  return (
    <>
      <Router>
        <MastHead />

        <Switch>
          <Route exact path="/" component={RecentPosts} />
          <Route exact path="/:year/:month" component={Month} />
          <Route exact path="/:year/:month/:day/:title" component={SinglePost} />
          <Route exact path="/archives" component={Archives} />
        </Switch>

        <SiteFooter />
      </Router>
    </>
  )
};

ReactDOM.render(<Index />, document.getElementById('root'));

