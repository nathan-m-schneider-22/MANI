import cv2
cap = cv2.VideoCapture(0)

# Camera class for all camera-related code


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    # Capture the current frame and transform it as needed
    def capture_image(self):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        return rgb

    # Release the components utilized by the camera
    def teardown(self):
        self.cap.release()
        cv2.destroyAllWindows()
