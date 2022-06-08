import threading
import cv2
from .camera import RPI_Camera, LaptopCamera
import interpreter.constants as constants

from flask import Flask, Response

outputFrame = None
lock = threading.Lock()
display_raw_frame = False
frame = None

if constants.RPI_DETECTED:
    camera = RPI_Camera()
else:
    camera = LaptopCamera()

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def generate():
    global lock, outputFrame, frame, camera, display_raw_frame

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            
            frame = camera.capture_image()
            if display_raw_frame and frame is not None:
                outputFrame = frame.copy()
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')
