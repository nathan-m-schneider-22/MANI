from .camera import Camera
import cv2
import time
import numpy as np
import mediapipe as mp

from joblib import load
from .new_model.preprocess.feature_extractor import extract_features

# Interpreter class to parse images into signs, and build signs

FRAME_RATE = 30


class Interpreter:
    def __init__(self, display_instance):
        self.display_instance = display_instance
        self.camera = Camera()
        checkpoint_path = "./interpreter/new_model/output/model.joblib"
        self.model = load(checkpoint_path)
        
        # mediapipe model
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def display_frame(self, frame):
        frame = cv2.resize(frame, (480, 360))                # Resize image
        cv2.imshow('frame', frame)
        cv2.moveWindow('frame', 240, 200)
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

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            exit(0)
        
        result = 'no hand'
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # making prediction 
                features, _ = extract_features([hand_landmarks], ['a'], input_type ='inference')
                preds = self.model.predict_proba(features)
                result = self.model.classes_[np.argmax(preds)]
                break

        return result

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM
    def wait_for_input(self):
        print("Waiting for user input")
        # For this example, lets assume we always wait 5 seconds before a user gives an input
        for _ in range(5*FRAME_RATE):
            frame = self.camera.capture_image()
            self.display_frame(frame)

    # Captures the full sign input from the user, utilizes more complicated FSM logic
    def capture_full_input(self):
        print("Capturing input")
        input = ""
        frame_count = 40
        # for this example lets just capture 5 letters 1 second apart
        for _ in range(3):
            for _ in range(frame_count):
                result = self.parse_frame()
            input += result
            self.display_instance.display_query(input)
            time.sleep(.5)
        return input

    def teardown(self):
        self.camera.teardown()
