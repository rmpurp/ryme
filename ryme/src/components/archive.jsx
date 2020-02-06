import React from 'react';
import { FOOTER } from '../config';
import lodash from 'lodash';
import axios from 'axios';
import {SITE_TITLE} from '../config';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";

class Archive extends React.Component {
  state = {
    entries: []
  }


  componentDidMount() {
    document.title = `${SITE_TITLE} Archives`

    axios.get('/api/archive').then(response => {
      let entries = response.data.content;
      this.setState({
        entries: lodash.sortBy(entries, ["year", "month"]).reverse()
      })
    })
  }

  render() {
    let rendered = this.state.entries.map(entry => {
      return (
        <li key={JSON.stringify(entry)}>
          <Link to={`/${entry.year}/${entry.month}`}>
            {`${entry.year}-${entry.month}`}
          </Link>
        </li>
      )
    })
    return (
      <ul className="ryme-archive">
        {rendered}
      </ul>
    );
  }
}

export default Archive;
