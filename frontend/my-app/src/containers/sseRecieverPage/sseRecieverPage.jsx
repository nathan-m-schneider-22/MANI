import { Spinner } from '@geist-ui/react';
import React from 'react';
import loading from './loading.gif';
import './ssePage.scss';
class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      input: "",
      fsm_state: "sleep",
      response: "",
      loading: false
    };
    this.ws = new WebSocket("ws://127.0.0.1:5001/");
  }

  render() {
    this.ws.onopen = () => {
      console.log('Opened Connection!')
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      // console.log(data)
      if (data.message_type === 'state') {
        this.setState({
          fsm_state: data.state
        })
        if (data.state === 'sleep') {
          this.setState({
            input: '',
          })
        }
        if (data.state === 'green') {
          this.setState({
            top_letter: data.letter
          })
        }
        if (data.state === 'yellow') {
          this.setState({
            top_letter: data.letters[0],
            second_letter: data.letters[1]
          })
        }
        if (data.state === 'save') {
          this.setState({
            input: data.input
          })
        }
        if (data.state === 'send') {
          this.setState({
            input: data.input
          })
        }
        if (data.state === 'display') {
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
      <div>
      <h1 className="header"> Welcome to Project MANI</h1>
        <div className='sse-page'>

            <div className='video-container'>
              <img src={'//127.0.0.1:5555/stream'} className='video'/>
            </div>
            
            <div className='text_container'>
              {this.state.fsm_state === "sleep" && (
                <div>
                  <h1><span className='cursor'>_</span></h1>
                  <h2>Hold your hand in the screen to start signing</h2>
                </div>
              )}
              {this.state.fsm_state === "wait" && (
                <div>
                  <h1>{this.state.input}<span className='cursor'>_</span></h1>
                  <h2> Hold you hand in the screen to start signing</h2>
                </div>
              )}
              {this.state.fsm_state === "green" && (
                <div>
                  <h1>{this.state.input}<span className='cursor'>_</span></h1>
                  <p className='top-letter'>{this.state.top_letter}</p>
                  {/* <h2>{this.state.response}</h2> */}
                </div>
              )}
              {this.state.fsm_state === "save" && (
                <div>
                  <h1>{this.state.input}<span className='cursor'>_</span></h1>

                  {/* <h2>{this.state.response}</h2> */}
                </div>
              )}
              {this.state.fsm_state === "send" && (
                <div>
                  <h1>{this.state.input}</h1>
                  <br/>

                  <Spinner className="spinner" style={{margin: 'auto'}}/>
                </div>
              )}
              {this.state.fsm_state === "display" && (
                <div>
                  <div>
                    <h2>{this.state.input}</h2>
                    {/* <h2>{this.state.response}</h2> */}
                    <div>
                    <iframe className="assistant-frame" title="MANI" srcdoc={this.state.response}></iframe>
                    </div>
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
