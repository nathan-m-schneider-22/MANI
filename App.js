import React, { useEffect, useRef} from "react";
import "../node_modules/jszip/dist/jszip.js"
import saveAs from "file-saver"

const App = () => {
  const videoRef = useRef(null);
  const photoRef = useRef(null);
  const stripRef = useRef(null);
  const colorRef = useRef(null);

  useEffect(() => {
    getVideo();
  }, [videoRef]);

  const getVideo = () => {
    navigator.mediaDevices
      .getUserMedia({ video: { width: 200 } })
      .then(stream => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("error:", err);
      });
  };

  const paintToCanvas = () => {
    let video = videoRef.current;
    let photo = photoRef.current;
    let ctx = photo.getContext("2d");

    const width = 320;
    const height = 240;
    photo.width = width;
    photo.height = height;

    return setInterval(() => {
      let color = colorRef.current;

      ctx.drawImage(video, 0, 0, width, height);
      let pixels = ctx.getImageData(0, 0, width, height);

      color.style.backgroundColor = `rgb(${pixels.data[0]},${pixels.data[1]},${
        pixels.data[2]
      })`;
      color.style.borderColor = `rgb(${pixels.data[0]},${pixels.data[1]},${
        pixels.data[2]
      })`;
    }, 200);
  };

  const takePhoto = () => {
    let photo = photoRef.current;
    let strip = stripRef.current;

    const data = photo.toDataURL("image/jpeg");
    console.warn(data);
    const link = document.createElement("a");
    link.href = data;
    link.setAttribute("download", "myWebcam");
    link.innerHTML = `<img src='${data}' alt='thumbnail'/>`;
    strip.insertBefore(link, strip.firstChild);
    document.querySelector('.start-button').setAttribute("disabled", "true")
    document.querySelector('.stop-button').removeAttribute("disabled")
    var JSZip = require("jszip");
    var zip = new JSZip();
    var img = zip.folder("images");
    img.file("smile.gif", data, {base64: true});
    zip.generateAsync({type:"blob"})
    .then(function(content) {
    // see FileSaver.js
    saveAs(content, "example.zip");
  });

  };

  const stopPhoto = () => {
    document.querySelector('.stop-button').setAttribute("disabled", "true")
    document.querySelector('.start-button').removeAttribute("disabled")

  };


  return (
      <div className="webcam-video">
        <button className = "start-button" onClick={() => takePhoto()}>Start taking photos</button>
        <button className = "stop-button" onClick={() => stopPhoto()}>Stop taking photos</button>
        <video
          onCanPlay={() => paintToCanvas()}
          ref={videoRef}
          className="player"
        />
        <canvas ref={photoRef} className="photo" />
        <div className="photo-booth">
          <div ref={stripRef} className="strip" />
        </div>
        </div>
  );
};

export default App;

