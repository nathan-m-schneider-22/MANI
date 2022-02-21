from turtle import update
from .camera import Camera
import cv2
import time
from .model.LetterPredictor import LetterPredictor
import numpy as np
import random
# Interpreter class to parse images into signs, and build signs

FRAME_RATE = 30
YELLOW_ACC_THRESHOLD = .8


class Interpreter:
    def __init__(self, display_instance):
        self.display_instance = display_instance
        self.camera = Camera()
        checkpoint_path = "interpreter/model/sample-asl-combodata.ckpt"
        self.model = LetterPredictor(checkpoint_path)

    def display_frame(self, frame):
        frame = cv2.resize(frame, (480, 360))                # Resize image
        cv2.imshow('frame', frame)
        # cv2.moveWindow('frame', 240, 200)
        cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            exit(0)

    # Parses the current frame from ASL to a letter
    def parse_frame(self):
        frame = self.camera.capture_image()
        self.display_frame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = self.model.predict(frame)  # pass to Letter Predictor model

        return result

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM
    def wait_for_input(self):
        print("Waiting for user input")
        self.display_instance.display_state("sleep")
        # For this example, lets assume we always wait 5 seconds before a user gives an input
        for _ in range(3*FRAME_RATE):
            frame = self.camera.capture_image()
            self.display_frame(frame)

        self.display_instance.display_state("wait")
        for _ in range(3*FRAME_RATE):
            frame = self.camera.capture_image()
            self.display_frame(frame)

    def green_capture(self, timeout=1):
        print("green capture")
        st = time.time()
        letter = ""
        results = []
        self.display_instance.display_state("green",
                                            {"letter": letter, "timeout": timeout})

        while time.time() - st < timeout:

            result = self.parse_frame()
            results.append(result)
            self.display_instance.display_state("green",
                                                {"letter": result}, update=True)
        return results

    def yellow_capture(self, top, second, timeout=2):
        results = []
        print("yellow capture")
        self.display_instance.display_state("yellow",
                                            {"letters": [top, second], "timeout": timeout})

        st = time.time()
        while time.time() - st < timeout:
            print("yellow loop")
            result = self.parse_frame()
            results.append(result)

        return random.sample([top, second], 1)

    # Captures the full sign input from the user, utilizes more complicated FSM logic
    def capture_full_input(self):
        print("Capturing input")
        input = ""

        for _ in range(3):
            results = self.green_capture()
            top_letter = max(results, key=results.count)

            if results.count(top_letter)/len(results) < YELLOW_ACC_THRESHOLD:  # Begin yellow mode
                other_results = [r for r in results if r != top_letter]
                second_top_letter = max(other_results, key=other_results.count)

                result = self.yellow_capture(top_letter, second_top_letter)
            else:
                result = top_letter

            print("saving letter")
            input += result
            self.display_instance.display_state(
                "save", {"letter": result, "input": input})
            time.sleep(.2)

        self.display_instance.display_state("send", {"input": input})
        time.sleep(.5)

        return input

    def teardown(self):
        self.camera.teardown()
