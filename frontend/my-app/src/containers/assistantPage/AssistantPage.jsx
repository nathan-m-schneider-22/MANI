import React, { useEffect, useRef, useState } from "react";
import { Page, Text, Card, Spinner } from "@geist-ui/react";
import { useMediaQuery } from "react-responsive";
import "./assistantPage.css";

export default function AssistantPage() {
  const isLaptop = useMediaQuery({ query: "(min-width: 800px)" });
  const SAMPLING_RATE = 500; // sample 4x per minute

  const [displayMode, setDisplayMode] = useState("INPUT");

  const [photo, setPhoto] = useState(null);
  const videoRef = useRef(null);
  const photoRef = useRef(null);
  const stripRef = useRef(null);
  const colorRef = useRef(null);

  useEffect(() => {
    getVideo();
  }, [videoRef]);

  useEffect(() => {
    const interval = setInterval(() => {
      let video = videoRef.current;
      let photo = photoRef.current;
      if (photo) {
        let ctx = photo.getContext("2d");

        const width = 320 / 2;
        const height = 240 / 2;
        photo.width = width;
        photo.height = height;

        ctx.drawImage(video, 0, 0, width, height);

        setPhoto(photoRef.current);
        sendPhoto();
      }
    }, SAMPLING_RATE);
    return () => clearInterval(interval);
  }, []);

  // for demo only
  useEffect(() => {
    let counter = 0;
    const interval = setInterval(() => {
      switch (counter % 3) {
        case 0:
          setDisplayMode("LOADING");
          break;
        case 1:
          setDisplayMode("OUTPUT");
          break;
        case 2:
          window.location.reload(false);
          setDisplayMode("INPUT");
          break;
        default:
          setDisplayMode("INPUT");
          break;
      }
      counter++;
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const sendPhoto = () => {
    console.log("sent photo to backend!");
  };

  const getVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: { width: 400 } })
      .then((stream) => {
        let video = videoRef.current;
        if (video) {
          video.srcObject = stream;
          video.play();
        }
      })
      .catch((err) => {
        console.error("error:", err);
      });
  };

  return (
    <Page.Content
      style={{
        overflow: "hidden",
      }}
    >
      <Card>
        <Card.Content>
          <center>
            <Text font="50px" margin="0em">
              Welcome to <b style={{ color: "pink" }}> MANI!</b>
            </Text>
            <div class="head-text">
              <video
                style={{
                  width: "50vw",
                  filter: displayMode === "INPUT" ? "auto" : "blur(15px)",
                }}
                ref={videoRef}
                className="player"
              ></video>
              <div class="text-on-image">
                {displayMode === "LOADING" && (
                  <>
                    <Text font="40px" margin="0em">
                      Loading your response...
                    </Text>
                    <Spinner />
                  </>
                )}
                {displayMode === "OUTPUT" && (
                  <>
                    <Text font="50px" margin="0em">
                      Calling an Uber to your location...
                    </Text>
                  </>
                )}
              </div>
            </div>
            <Text>What is sent to the backend: </Text>
            <canvas ref={photoRef} className="photo" />
          </center>
        </Card.Content>
      </Card>
    </Page.Content>
  );
}
