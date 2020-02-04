import React from 'react';
import {AUTHOR, SITE_TITLE} from '../config'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";

class MastHead extends React.Component {
  render() {
    return (
      <div className="ryme-masthead">
         <Link to="/" id="ryme-site-title">{SITE_TITLE}</Link>
        <div className="ryme-author">
          {AUTHOR}
      </div>
      <div className="ryme-hairline"/>
      </div>

    );
  }
}

export default MastHead;
