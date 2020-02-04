import React from 'react';
import {AUTHOR, SITE_TITLE} from '../config'

class MastHead extends React.Component {
  render() {
    return (
      <div className="ryme-masthead">
        <div className="ryme-site-title">
         {SITE_TITLE} 
        </div>
        <div className="ryme-author">
          {AUTHOR}
      </div>
      <div className="ryme-hairline"/>
      </div>

    );
  }
}

export default MastHead;
