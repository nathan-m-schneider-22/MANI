import { Spinner } from "@geist-ui/react";
import React from "react";
import loading from "./loading.gif";
import * as Constants from "../../constants";
import "./ssePage.scss";

class sseRecieverPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      input: "",
      fsm_state: "sleep",
      response: "",
      loading: false,
    };
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
        }
        if (data.state === Constants.FSM_DISPLAY) {
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
      <div>
        <h1 className="header"> Welcome to Project MANI</h1>
        <div className="sse-page">
          <div className="video-container">
            <img src={Constants.STREAM_URL} className="video" />
          </div>

          <div className="text_container">
            {this.state.fsm_state === Constants.FSM_SLEEP && (
              <div>
                <h1>
                  <span className="cursor">_</span>
                </h1>
                <h2>Sign "hello" to start input</h2>
              </div>
            )}
            {this.state.fsm_state === Constants.FSM_WAIT && (
              <div>
                <h1>
                  {this.state.input}
                  <span className="cursor">_</span>
                </h1>
                <h2> Hold you hand in the screen to start signing</h2>
              </div>
            )}
            {this.state.fsm_state === Constants.FSM_GREEN && (
              <div>
                <h1>
                  {this.state.input}
                  <span className="cursor">_</span>
                </h1>
                <p className="top-letter">{this.state.top_letter}</p>
                {/* <h2>{this.state.response}</h2> */}
              </div>
            )}
            {this.state.fsm_state === Constants.FSM_SAVE && (
              <div>
                <h1>
                  {this.state.input}
                  <span className="cursor">_</span>
                </h1>

                {/* <h2>{this.state.response}</h2> */}
              </div>
            )}
            {this.state.fsm_state === Constants.FSM_SEND && (
              <div>
                <h1>{this.state.input}</h1>
                <br />

                <Spinner className="spinner" style={{ margin: "auto" }} />
              </div>
            )}
            {this.state.fsm_state === Constants.FSM_DISPLAY && (
              <div>
                <div>
                  <h2>{this.state.input}</h2>
                  {/* <h2>{this.state.response}</h2> */}
                  <div>
                    <iframe
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
      </div>
    );
  }
}

export default sseRecieverPage;
