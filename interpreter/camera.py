import time
import cv2
import numpy as np
# cap = cv2.VideoCapture(0)

# Camera class for all camera-related code
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()


class Camera:
    def __init__(self):
        self.cap = picam2
        # if not self.cap.isOpened():
        #     raise IOError("Cannot open webcam")
        # else:
        #     print("opening camera")
        time.sleep(2.0) # wait for camera to warm up

    # Capture the current frame and transform it as needed
    def capture_image(self):
        # try:
        frame = self.cap.capture_array()
        frame = cv2.flip(frame, 0)

        return frame
        # except:
        #     print('capturing frame failed')
        #     return None

    # Release the components utilized by the camera
    def teardown(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__=="__main__":

    cam = Camera()
    while True:
        frame = cam.capture_image()
        print("frame")
        print(np.shape(frame))
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for 1 millisecond
            break



