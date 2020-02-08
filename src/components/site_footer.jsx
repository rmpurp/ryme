import React from 'react';

import { Link } from 'react-router-dom';

class SiteFooter extends React.Component {
  render() {
    return (
      <div className="ryme-site-footer">
        <div className="ryme-hairline" />
        <Link to="/archives">Archives</Link>
      </div>
    );
  }
}

export default SiteFooter;
