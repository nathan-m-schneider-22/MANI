from turtle import update
from .camera import Camera
import cv2
import time
import numpy as np
import random
import mediapipe as mp

from joblib import load
from . import streamer
from .new_model.preprocess.feature_extractor import extract_features

# Interpreter class to parse images into signs, and build signs

FRAME_RATE = 30
YELLOW_ACC_THRESHOLD = .8

class Interpreter:
    def __init__(self, display_instance):
        self.display_instance = display_instance
        # self.camera = Camera()
        checkpoint_path = "./interpreter/new_model/output/model.joblib"
        self.model = load(checkpoint_path)

        # mediapipe model
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        # interpreter sentence inference variables
        self.state = np.array([1/26 for _ in range(26)])
        self.curr_letter = ''
        self.curr_input = ''
        self.start_time = time.time()

        # interpreter sentence hyperparameters
        self.alpha = .04
        self.theta = .35

    def display_frame(self, frame):
        if frame is not None:
            with streamer.lock:
                streamer.outputFrame = frame.copy()
        # frame = cv2.resize(frame, (480, 360))                # Resize image
        # cv2.imshow('frame', frame)
        # cv2.moveWindow('frame', 30, 80)
        # cv2.setWindowProperty('frame', cv2.WND_PROP_TOPMOST, 1)

        # k = cv2.waitKey(1)
        # if k % 256 == 27:
        #     print("Escape hit, closing...")
        #     exit(0)

    # Parses the current frame from ASL to a letter
    def parse_frame(self):
        # frame = self.camera.capture_image()
        frame = streamer.frame
        if frame is not None:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            result = 'no hand'
            results = self.hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())

                    # making prediction
                    features, _ = extract_features(
                        [hand_landmarks], ['a'], input_type='inference')
                    preds = self.model.predict_proba(features)
                    self.state = self.state + self.alpha*(preds-self.state)
                    pred = self.model.classes_[np.argmax(self.state)]
                    self.display_instance.display_state(
                        'green', {"letter": pred, "input": self.curr_input})
                    if pred == '_':
                        pred = ' '
                    if time.time()-self.start_time > 3 and np.max(self.state) > .35:
                        if self.curr_letter != pred:
                            self.curr_letter = pred

                            if self.curr_letter == 'x':
                                self.curr_input = self.curr_input[:-1]
                                self.curr_letter = ''
                                self.start_time = time.time()
                            else:
                                self.curr_input += pred

                            self.display_instance.display_state(
                                "save", {"input": self.curr_input})
                            self.display_instance.display_query(self.curr_input)

                    break

            self.display_frame(frame)
            if results.multi_hand_landmarks == None:
                print("FINISHE")
                state = np.array([1/26 for _ in range(26)])
                self.curr_letter = ""
                self.start_time = time.time()
                pred = 'clear'

                self.display_instance.display_query(self.curr_input)
                self.input_finished = 1

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM

    def is_hand_in_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame)
        hand_in_frame = results.multi_hand_landmarks != None
        return hand_in_frame

    def wait_for_input(self):
        print("Waiting for user input")
        # For this example, lets assume we always wait 5 seconds before a user gives an input
        # frame = self.camera.capture_image()
        frame = streamer.frame
        while frame is None:
            frame = streamer.frame
            time.sleep(.1)
            
        self.display_frame(frame)

        start_time = time.time()
        while not self.is_hand_in_frame(frame):
            frame = streamer.frame
            self.display_frame(frame)

            # Captures the full sign input from the user, utilizes more complicated FSM logic
    def capture_full_input(self):
        print("Capturing input")
        start_time = time.time()
        self.curr_letter = ''
        self.curr_input = ''
        self.input_finished = 0

        while not self.input_finished:
            self.parse_frame()

        return self.curr_input

    def teardown(self):
        streamer.camera.teardown()
