import React from 'react';
import loading from './loading.gif'
class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      response: "",
      loading: false
    };
    this.ws = new WebSocket("ws://127.0.0.1:5000/");
  }

  render() {
    this.ws.onopen = () => {
      console.log('Opened Connection!')
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      // console.log(data)
      if (data.message_type == 'state') {
        this.setState({
          fsm_state: data.state
        })
        if (data.state == 'green') {
          this.setState({
            top_letter: data.letter
          })
        }
        if (data.state == 'yellow') {
          this.setState({
            top_letter: data.letters[0],
            second_letter: data.letters[1]
          })
        }
        if (data.state == 'save') {
          this.setState({
            letter: data.letter,
            input: data.input
          })
        }
        if (data.state == 'send') {
          this.setState({
            input: data.input
          })
        }
        if (data.state == 'display') {
          this.setState({
            response: data.response
          })
        }
      }

      this.setState({ currentData: JSON.parse(event.data) });
      console.log(this.state)
    };

    this.ws.onclose = () => {
      console.log('Closed Connection!')
    };

    return (
      <div className='App'>
        <div className='row'>
          <div className='col'></div>
          <div className='col'>
            <h1> Welcome to Project Mani</h1>
            {this.state.fsm_state == "sleep" && (
              <div>
                <h2> Hold your hand in the screen to start signing</h2>
              </div>
            )}
            {this.state.fsm_state == "wait" && (
              <div>
                <h2> Hold you hand in the screen to start signing</h2>
              </div>
            )}
            {this.state.fsm_state == "green" && (
              <div>
                <h1>{this.state.input}<span>_</span></h1>
                <p className='top-letter'>{this.state.top_letter}</p>
              </div>
            )}
            {this.state.fsm_state == "yellow" && (
              <div>
                <h1>{this.state.input}<span>_</span></h1>
                <p className='letter-one'>{this.state.top_letter}</p>
                <p className='letter-two'>{this.state.second_letter}</p>
              </div>
            )}
            {this.state.fsm_state == "save" && (
              <div>
                <h1>{this.state.input}</h1>
              </div>
            )}
            {this.state.fsm_state == "send" && (
              <div>
                <h1>{this.state.input}</h1>
                <h2>Waiting for response from the server</h2>
              </div>
            )}
            {this.state.fsm_state == "sleep" && (
              <div>
                <div>
                  <h1>{this.state.input}</h1>
                  <h1>{this.state.response}</h1>
                </div>
              </div>
            )}
          </div>
        </div>

      </div>
    )

  }
}

export default sseRecieverPage;
