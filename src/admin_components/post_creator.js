import React from 'react';
import moment from 'moment';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import Axios from 'axios';

export class PostCreator extends React.Component {
  state = {
    date: new Date(),
    slug: '',
    content: '@@Title=\n@@Date='
  }

  handleDateChange = date => {
    this.setState({ date });
  }

  handleSlugChange = event => {
    this.setState({ slug: event.target.value });
  }

  handleContentChange = event => {
    this.setState({ content: event.target.value });
  }

  uploadPost = () => {
    if (this.state.slug === '' || this.state.content === '') {
      alert('Slug or content is empty');
      return;
    }

    const date = moment(this.state.date);
    const params = {
      year: date.format('YYYY'),
      month: date.format('MM'),
      day: date.format('DD'),
      slug: this.state.slug,
      content: this.state.content,
    };

    Axios.post('/admin-api/create-post', params)
      .then(() => {
        alert('Success!');
        
      })
      .catch((err) => {
        alert(err);
      });
  }

  render() {
    return (
      <>
        <h1>Create New Post (Same slug and date will overwrite old post):</h1>
        <span>Date: </span>
        <DatePicker
          selected={this.state.date}
          onChange={this.handleDateChange}
        />

        <br></br>
        <span> Slug: </span>
        <input type="text" value={this.state.slug} onChange={this.handleSlugChange} />

        <br/>
        Content:
        <br/>
        <textarea value={this.state.content} onChange={this.handleContentChange} rows="40" cols="100"/>

        <br/>
        <button onClick={this.uploadPost}>Upload</button>
      </>
    );
  }
}
