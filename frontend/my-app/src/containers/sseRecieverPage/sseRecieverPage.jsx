import { Spinner, Image } from "@geist-ui/react";
import React from "react";
import loading from "./loading.gif";
import * as Constants from "../../constants";
import "./ssePage.scss";
import mani_logo from '../../assets/mani_logo.png';

class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      input: "",
      fsm_state: "sleep",
      response: "",
      loading: false,
      hand: "left",
    };
    this.history = [];
    this.ws = new WebSocket(Constants.WEB_SOCKET);
  }

  render() {
    this.ws.onopen = () => {
      console.log("Opened Connection!");
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // console.log(data)
      if (data.message_type === Constants.MESSAGE_TYPE) {
        this.setState({
          fsm_state: data.state,
        });
        if (data.state === Constants.FSM_SLEEP) {
          this.setState({
            input: "",
          });
        }
        if (data.state === "hand") {
          this.setState({
            hand: data.hand,
          });
        }
        if (data.state === Constants.FSM_GREEN) {
          this.setState({
            top_letter: data.letter,
          });
        }
        if (data.state === Constants.FSM_YELLOW) {
          this.setState({
            top_letter: data.letters[0],
            second_letter: data.letters[1],
          });
        }
        if (data.state === Constants.FSM_SAVE) {
          this.setState({
            input: data.input,
          });
        }
        if (data.state === Constants.FSM_SEND) {
          this.setState({
            input: data.input,
          });
          this.history.push(this.input);
        }
        if (data.state === Constants.FSM_DISPLAY) {
          this.history.push(this.response);
          this.setState({
            response: data.response,
          });
        }
      }

      this.setState({ currentData: JSON.parse(event.data) });
      console.log(this.state);
    };

    this.ws.onclose = () => {
      console.log("Closed Connection!");
    };

    return (
      <div className="sse-page">
        {this.state.hand === "left" && (
          <div className="video-container">
            <img src={Constants.STREAM_URL} className="video" />
          </div>
        )}
        <div className="text_container">
            <img src = {mani_logo} style ={{
              width: '50%',
              margin: 'auto'
            }}/>
            <div className="input-response">
              {this.state.fsm_state === Constants.FSM_SLEEP && (
                <div>
                  <h1>
                    Input:&nbsp;
                    <span className="cursor">_</span>
                  </h1>
                  <h2>Sign "hello" to start input</h2>
                </div>
              )}
              {this.state.fsm_state === Constants.FSM_WAIT && (
                <div>
                  <h1>
                    Input:&nbsp;{this.state.input}
                    <span className="cursor">_</span>
                  </h1>
                  <h2> Hold you hand in the screen to start signing</h2>
                </div>
              )}
              {this.state.fsm_state === Constants.FSM_GREEN && (
                <div>
                  <h1>
                    Input:&nbsp;
                    {this.state.input}
                    <span className="cursor">_</span>
                  </h1>
                  <p>
                    Current Sign:&nbsp;
                    <span className="top-letter">{this.state.top_letter}</span>
                  </p>
                  {/* <h2>{this.state.response}</h2> */}
                </div>
              )}
              {this.state.fsm_state === Constants.FSM_SAVE && (
                <div>
                  <h1>
                    Input:&nbsp;
                    {this.state.input}
                    <span className="cursor">_</span>
                  </h1>

                  {/* <h2>{this.state.response}</h2> */}
                </div>
              )}
              {this.state.fsm_state === Constants.FSM_SEND && (
                <div>
                  <h1>Input: {this.state.input}</h1>
                  <br />

                  <Spinner className="spinner" style={{ margin: "auto" }} />
                </div>
              )}
              {this.state.fsm_state === Constants.FSM_DISPLAY && (
                <div>
                  <div>
                    <h1>Input: {this.state.input}</h1>
                    {/* <h2>{this.state.response}</h2> */}
                    <div>
                      <iframe
                        // this is a very strange styling trick to make sure that the frame is on the correct side
                        // the frame is made to fit the whole screen, then scaled to half size, leaving it in the middle of the screen,
                        // need to move it 25% Left or right if we want it to be on the right side
                        style={{ right: this.state.hand == 'right' ? '25%' : '-25%' }}
                        className="assistant-frame"
                        title="MANI"
                        srcdoc={this.state.response}
                      ></iframe>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
          {this.state.hand === "right" && (
            <div className="video-container">
              <img src={Constants.STREAM_URL} className="video" />
            </div>
          )}
        </div>
    );
  }
}

export default sseRecieverPage;
/*<img className="logo" src={maniLogo} />*/
