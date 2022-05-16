import time
import cv2
cap = cv2.VideoCapture(0)

# Camera class for all camera-related code


class Camera:
    def __init__(self):
        self.cap = cap
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        else:
            print("opening camera")
        time.sleep(2.0) # wait for camera to warm up

    # Capture the current frame and transform it as needed
    def capture_image(self):
        try:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 0)

            return frame
        except:
            print('capturing frame failed')
            return None

    # Release the components utilized by the camera
    def teardown(self):
        self.cap.release()
        cv2.destroyAllWindows()
