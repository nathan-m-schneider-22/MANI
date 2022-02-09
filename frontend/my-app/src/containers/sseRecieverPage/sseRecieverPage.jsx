import React from 'react';

class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentData: []
    };
    this.ws = new WebSocket("ws://127.0.0.1:5000/");
  }

  render() {
    this.ws.onopen = () => {
      console.log('Opened Connection!')
    };

    this.ws.onmessage = (event) => {
      console.log(event.data)
      this.setState({ currentData: JSON.parse(event.data) });
    };

    this.ws.onclose = () => {
      console.log('Closed Connection!')
    };

    const columns = [
      { Header: 'Name', accessor: 'name' },
      { Header: 'Number', accessor: 'number' }
    ]
    console.log(this.state.currentData);
    return (
      <div className="App">
        <p>TBD</p>
      </div>
    );
  }
}

export default sseRecieverPage;
