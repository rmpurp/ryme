import React from 'react';
import lodash from 'lodash';
import axios from 'axios';
import { SITE_TITLE } from '../config';

import { Link } from 'react-router-dom';

/**
 * The archive of the blog, displaying links to months with posts.
 */
class Archive extends React.Component {
  state = {
    entries: []
  }

  componentDidMount() {
    document.title = `${SITE_TITLE} Archives`;

    axios.get('/api/archive').then(response => {
      let entries = response.data.content;
      this.setState({
        entries: lodash.sortBy(entries, ['year', 'month']).reverse()
      });
    });
  }

  render() {
    let rendered = this.state.entries.map(entry => {
      return (
        <li key={JSON.stringify(entry)}>
          <Link to={`/${entry.year}/${entry.month}`}>
            {`${entry.year}-${entry.month}`}
          </Link>
        </li>
      );
    });
    return (
      <ul className="ryme-archive">
        {rendered}
      </ul>
    );
  }
}

export default Archive;
