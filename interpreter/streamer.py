import threading
import cv2
import time
from .camera import Camera
from flask import Flask, Response

outputFrame = None
lock = threading.Lock()
display_raw_frame = False
frame = None
camera = Camera()

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def generate():
    global lock, outputFrame, frame, camera, display_raw_frame

    # loop over frames from the output stream
    prev_frame_time = 0
    new_frame_time = 0
    frame_count = 0
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
            
            # new_frame_time = time.time()
            # fps = 1/(new_frame_time - prev_frame_time)
            # prev_frame_time = new_frame_time
            # fps = str(int(fps))
            # print(fps)
            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')
