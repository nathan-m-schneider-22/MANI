import React from 'react';
import loading from './loading.gif'
class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      response: "",
      loading:false
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
        this.setState({query:data.content,loading:false})
      }
      if (data.type === "response"){
        this.setState({response:data.content,loading:false})
      }
      if (data.type === "reset"){
        this.setState({response:"",query:"",loading:false})
      }
      if (data.type === "loading"){
        this.setState({loading:true})
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
        {this.state.loading && <img width={30} src={loading}></img>}
      </div>
    );
  }
}

export default sseRecieverPage;
