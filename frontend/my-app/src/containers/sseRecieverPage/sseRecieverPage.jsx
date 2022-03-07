import { Spinner } from "@geist-ui/react";
import React, { useState, useRef } from "react";
import loading from "./loading.gif";
import "./ssePage.scss";

export default function SseRecieverPage(props) {
  const [input, setInput] = useState("");
  const [fsmState, setFsmState] = useState("sleep");
  const [response, setResponse] = useState("sleep");
  const [loading, setLoading] = useState(false);
  const [topLetter, setTopLetter] = useState("");
  const [secondLetter, setSecondLetter] = useState("");
  const [currentData, setCurrentData] = useState();

  const ws = useRef(new WebSocket("ws://127.0.0.1:5001/"));

  ws.current.onopen = () => {
    console.log("Opened Connection!");
  };

  ws.current.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.message_type === "state") {
      setFsmState(data.state);
      switch (data.state) {
        case "sleep":
          setInput("");
          break;
        case "green":
          setTopLetter(data.letter);
          break;
        case "yellow":
          setTopLetter(data.letters[0]);
          setSecondLetter(data.letters[1]);
          break;
        case "save":
          setInput(data.input);
          break;
        case "send":
          setInput(data.input);
          break;
        case "display":
          setResponse(data.response);
          break;
        default:
          console.log("invalid state");
      }
      setCurrentData(JSON.parse(event.data));
      console.log(currentData);
    }
  };

  ws.current.onclose = () => {
    console.log("Closed Connection!");
  };

  return (
    <>
      <div>
        <h1 className="header"> Welcome to Project MANI</h1>
        <div className="sse-page">
          <div className="video-container">
            <img src={"//127.0.0.1:5555/stream"} className="video" />
          </div>

          <div className="text_container">
            {fsmState === "sleep" && (
              <div>
                <h1>
                  <span className="cursor">_</span>
                </h1>
                <h2>Hold your hand in the screen to start signing</h2>
              </div>
            )}
            {fsmState === "wait" && (
              <div>
                <h1>
                  {input}
                  <span className="cursor">_</span>
                </h1>
                <h2> Hold you hand in the screen to start signing</h2>
              </div>
            )}
            {fsmState === "green" && (
              <div>
                <h1>
                  {input}
                  <span className="cursor">_</span>
                </h1>
                <p className="top-letter">{topLetter}</p>
                <h2>{response}</h2>
              </div>
            )}
            {fsmState === "save" && (
              <div>
                <h1>
                  {input}
                  <span className="cursor">_</span>
                </h1>

                <h2>{response}</h2>
              </div>
            )}
            {fsmState === "send" && (
              <div>
                <h1>{input}</h1>
                <br />

                <Spinner className="spinner" style={{ margin: "auto" }} />
              </div>
            )}
            {fsmState === "display" && (
              <div>
                <div>
                  <h2>{input}</h2>
                  {/* <h2>{response}</h2> */}
                  <div>
                    <iframe
                      className="assistant-frame"
                      title="MANI"
                      srcdoc={response}
                    ></iframe>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
