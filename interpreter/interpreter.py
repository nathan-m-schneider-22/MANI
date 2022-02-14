from .camera import Camera
import cv2
import time
# Interpreter class to parse images into signs, and build signs


class Interpreter:
    def __init__(self, display_instance):
        self.display_instance = display_instance
        self.camera = Camera()

    # Parses the current frame from ASL to a letter
    def parse_frame(self):
        frame = self.camera.capture_image()
        # cv2.imshow('frame', frame) # display the image if you want
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     exit(1)
        # ML STUFF GOES HERE
        result = "e"
        return result

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM
    def wait_for_input(self):
        print("Waiting for user input")
        # For this example, lets assume we always wait 5 seconds before a user gives an input
        time.sleep(5)

    # Captures the full sign input from the user, utilizes more complicated FSM logic
    def capture_full_input(self):
        input = ""
        # for this example lets just capture 5 letters 1 second apart
        for _ in range(5):
            result = self.parse_frame()
            input += result
            self.display_instance.display_query(input)
            time.sleep(1)
        return input

    def teardown(self):
        self.camera.teardown()
