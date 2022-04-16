from turtle import update

from .camera import Camera
from statistics import median
import math
import cv2
import time
import numpy as np
import random
import mediapipe as mp
import numpy.typing as npt

import interpreter.constants as constants

from joblib import load
from . import streamer
from .new_model.preprocess.feature_extractor import extract_features
from display.display import Display

# Interpreter class to parse images into signs, and build signs
class Interpreter:
    def __init__(self, display_instance: Display):
        self.display_instance = display_instance
        checkpoint_path = "./interpreter/new_model/output/model.joblib"
        self.model = load(checkpoint_path)

        # mediapipe model
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            model_complexity=constants.MODEL_COMPLEXITY,
            min_detection_confidence=constants.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=constants.MIN_TRACKING_CONFIDENCE)

        # interpreter sentence inference variables
        self.curr_letter = ''
        self.curr_input = ''

        self.med_delta_time = constants.INITIAL_TIME
        self.time_buffer = []
        self.prev_time = time.time()

        self.buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]

    def display_frame(self, frame: npt.NDArray):
        if frame is not None:
            with streamer.lock:
                streamer.outputFrame = frame.copy()

    # Parses the current frame from ASL to a letter
    def parse_frame(self):
        frame = streamer.frame
        if frame is not None:

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:

                curr_time = time.time()
                delta_time = curr_time-self.prev_time
                self.time_buffer.append(delta_time)
                self.prev_time = curr_time

                if len(self.time_buffer) > constants.TIME_LOOKBACK:
                    self.time_buffer.pop(0)
                    self.med_delta_time = median(self.time_buffer)
                
                match_size = int(math.floor(constants.TIME_PER_SIGN/self.med_delta_time))
                match_size = max(min((match_size, constants.MAX_BUFFER_SIZE)), constants.MIN_BUFFER_SIZE)

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
                    
                    cp = self.model.classes_[np.argmax(preds)]
                    self.buffer.pop(0)
                    self.buffer.append(cp)
                    self.display_instance.display_state(
                        'green', {"letter": cp, "input": self.curr_input})

                    if cp == '_':
                        cp = ' ' 

                    if all(x == self.buffer[-1] for x in self.buffer[-match_size:]):
                        if self.curr_letter != cp:
                            self.curr_letter = cp
                            if self.curr_letter == 'x':
                                self.curr_input = self.curr_input[:-1]
                                self.curr_letter = ''
                            else:
                                self.curr_input += self.curr_letter
                            self.buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]

                            self.display_instance.display_state(
                                "save", {"input": self.curr_input})

                    break

            self.display_frame(frame)
            if results.multi_hand_landmarks == None:
                self.curr_letter = ""
                self.start_time = time.time()
                self.display_instance.display_query(self.curr_input)
                self.input_finished = 1

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM
    def is_hand_in_frame(self, frame: npt.NDArray):
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
