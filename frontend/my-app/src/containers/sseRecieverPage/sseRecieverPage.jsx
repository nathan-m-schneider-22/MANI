import React from 'react';

class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      response: ""
    };
    this.ws = new WebSocket("ws://127.0.0.1:5000/");
  }

  render() {
    this.ws.onopen = () => {
      console.log('Opened Connection!')
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log(data)
      if (data.type === "query"){
        this.setState({query:data.content})
      }
      if (data.type === "response"){
        this.setState({response:data.content})
      }
      if (data.type === "reset"){
        this.setState({response:"",query:""})
      }
      this.setState({ currentData: JSON.parse(event.data) });
    };

    this.ws.onclose = () => {
      console.log('Closed Connection!')
    };
    
    return (
      <div className="App">
        <h1>{this.state.query}</h1>
        <h1>{this.state.response}</h1>

      </div>
    );
  }
}

export default sseRecieverPage;
