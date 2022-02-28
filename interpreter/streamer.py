import threading
import cv2
from flask import Flask, Response

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def generate():
    global lock, outputFrame

    # loop over frames from the output stream
    while True:
        print('here')
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            print('here')
            if outputFrame is None:
                continue
            print('yay')
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')
