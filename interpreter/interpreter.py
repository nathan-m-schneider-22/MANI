# from turtle import update

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

from threading import Thread, Lock
from joblib import load
from . import streamer
from .new_model.preprocess.feature_extractor import extract_features
from display.display import Display
from .pose_servo import turn_towards_pose

# Interpreter class to parse images into signs, and build signs
class Interpreter:
    def __init__(self, display_instance: Display):
        self.display_instance = display_instance
        
        checkpoint_path = "./interpreter/new_model/output/modelpy39.joblib"
        self.model = load(checkpoint_path)

        sequence_path = "./interpreter/new_model/output/sequence-model1.joblib"
        self.seq_model = load(sequence_path)

        # mediapipe model
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            # model_complexity=constants.MODEL_COMPLEXITY,
            min_detection_confidence=constants.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=constants.MIN_TRACKING_CONFIDENCE)
        
        self.hand_landmarks = None
        self.hand_landmark_lock = Lock()

        # interpreter sentence inference variables
        self.curr_letter = ''
        self.curr_seq_letter = ''
        self.curr_input = ''

        self.hand_assigned = False

        self.med_delta_time = constants.INITIAL_TIME
        self.time_buffer = []
        self.match_size = self.compute_match_size()
        self.prev_time = time.time()

        self.buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]
        self.prob_buffer = [0 for _ in range(constants.MAX_BUFFER_SIZE)]

        # sequence feature buffer
        self.feature_buffer = []
        self.sequence_buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]
        self.sequence_prob_buffer = [0 for _ in range(constants.MAX_BUFFER_SIZE)]

        self.word_is_signed = False
        self.word_signed = ''

    def choose_higher_hand(self, multi_hand_landmarks):
        max_height = 2 
        # height is between 0 and 1, 1 is all the way at bottom and 0 at top
        max_index = 0
        for (i, landmarks) in enumerate(multi_hand_landmarks):
            # because smaller numbers are higher, the hand must be a lower number than the max
            # using landmark[0] which is the wrist
            if landmarks.landmark[0].y < max_height:
                max_index = i
                max_height = landmarks.landmark[0].y
        return max_index  
            
    # Parses the current frame from ASL to a letter
    def parse_frame(self):
        frame = streamer.frame
        
        char_signed = False
        word_signed = False
        
        if frame is not None:

            # convert frame to RGB for processing
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame)

            # convert frame back to BGR for display 
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # if hand detected
            if results.multi_hand_landmarks:
                higher_hand = self.choose_higher_hand(results.multi_hand_landmarks)
                if not self.hand_assigned:
                    hand = results.multi_handedness[higher_hand]
                    handType=hand.classification[0].label
                    self.display_instance.display_state(
                        'hand', {"hand": handType.lower()})
                    self.hand_assigned = True

                # update match size value based on frame rate
                self.update_match_size()

                # get current hand landmarks
                hand_landmarks = results.multi_hand_landmarks[higher_hand]
                
                with self.hand_landmark_lock:
                    self.hand_landmarks = hand_landmarks

                # editting frame
                frame = self.frame_transform(frame)

                # making prediction
                features, _ = extract_features(
                    [hand_landmarks], ['a'], input_type='inference')
                preds = self.model.predict_proba(features)
                
                cp = self.model.classes_[np.argmax(preds)]
                cp_prob = np.max(preds)

                # update prob buffer
                self.prob_buffer.pop(0)
                self.prob_buffer.append(cp_prob)

                # update buffer
                self.buffer.pop(0)
                self.buffer.append(cp)

                # making sequence prediction
                if len(self.feature_buffer) == constants.SEQUENCE_INPUT_SIZE:
                    seq_features = np.array(self.feature_buffer)
                    seq_features = np.reshape(seq_features, seq_features.size).reshape(1, -1)
                    seq_preds = self.seq_model.predict_proba(seq_features)
                    seq_cp = self.seq_model.classes_[np.argmax(seq_preds)]
                    seq_cp_prob = np.max(seq_preds)

                    # update sequence buffer
                    self.sequence_buffer.pop(0)
                    self.sequence_buffer.append(seq_cp)

                    # update sequence prob buffer
                    self.sequence_prob_buffer.pop(0)
                    self.sequence_prob_buffer.append(seq_cp_prob)
                
                # update feature buffer
                if len(self.feature_buffer) == constants.SEQUENCE_INPUT_SIZE:
                    self.feature_buffer.pop(0)
                self.feature_buffer.append(features)

                # send current input to the display 
                self.display_instance.display_state(
                    'green', {"letter": cp, "input": self.curr_input})

                # convert '_' output to space
                if cp == '_':
                    cp = ' ' 

                # if we've seen cp self.match_size times in a row, add it
                if all(x == self.buffer[-1] for x in self.buffer[-self.match_size:]):
                    char_signed = True

                if all(x == self.sequence_buffer[-1] for x in self.sequence_buffer[-int(self.match_size/2):]) \
                    and self.sequence_buffer[-1] in ["j", "z"]:
                    word_signed = True

                if char_signed and word_signed:
                    word_weight = sum(self.sequence_prob_buffer[-int(self.match_size/2):])
                    char_weight = sum(self.prob_buffer[-int(self.match_size/2):])

                    if char_weight > word_weight:
                        if self.curr_letter != cp:
                            self.add_letter(cp) 

                    if word_weight > char_weight: 
                        if self.curr_seq_letter != seq_cp:
                            self.add_seq_letter(seq_cp)

                elif word_signed:
                    if self.curr_seq_letter != seq_cp:
                        self.add_seq_letter(seq_cp)

                elif char_signed:
                    if self.curr_letter != cp:
                        self.add_letter(cp)    
            

            if results.multi_hand_landmarks == None:
                self.hand_assigned = False
                self.curr_letter = ""
                self.curr_seq_letter = ""
                self.display_instance.display_query(self.curr_input)
                self.input_finished = 1

                with self.hand_landmark_lock:
                    self.hand_landmarks = None

    # Add letter to input query and display it
    def add_letter(self, cp: str):
        self.curr_letter = cp
        self.curr_seq_letter = ''
        if self.curr_letter == 'x':
            self.curr_input = self.curr_input[:-1]
            self.curr_letter = ''
        else:
            self.curr_input += self.curr_letter

        self.buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]
        self.sequence_buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]

        self.display_instance.display_state(
            "save", {"input": self.curr_input})

    def add_seq_letter(self, seq_cp: str):
        self.curr_seq_letter = seq_cp
        self.curr_letter = ''
        self.curr_input += self.curr_seq_letter

        self.buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]
        self.sequence_buffer = ['*' for _ in range(constants.MAX_BUFFER_SIZE)]

        self.display_instance.display_state(
            "save", {"input": self.curr_input})

    # Dynamically adjust buffer size based on frame rate
    def update_match_size(self):
        curr_time = time.time()
        delta_time = curr_time-self.prev_time
        self.time_buffer.append(delta_time)
        self.prev_time = curr_time

        if len(self.time_buffer) > constants.TIME_LOOKBACK:
            self.time_buffer.pop(0)
            self.med_delta_time = median(self.time_buffer)
        
        self.compute_match_size()

    def compute_match_size(self):
        match_size = int(math.floor(constants.TIME_PER_SIGN/self.med_delta_time))
        self.match_size = max(min((match_size, constants.MAX_BUFFER_SIZE)), constants.MIN_BUFFER_SIZE)

    # functions for displaying frames on a separate thread
    def display_frame_predict_thread(self, stop):
        self.display_frame_thread(stop, predict=True)

    def display_frame_wait_thread(self, stop):
        self.display_frame_thread(stop, predict=False)

    def display_frame_thread(self, stop, predict=False):
        while True:
            frame = streamer.frame
            if frame is not None:
                if predict:
                    frame = self.frame_transform(frame)
                    frame = self.mp_hand_transform(frame)
                with streamer.lock:
                    streamer.outputFrame = frame.copy()
            if stop():
                break

    def mp_hand_transform(self, frame):
        with self.hand_landmark_lock:
            if self.hand_landmarks != None:
                landmarks_style = self.mp_drawing_styles.get_default_hand_landmarks_style()
                for style in landmarks_style.values():
                    style.color = (128, 64, 128)
                    style.circle_radius = 0

                connections_style = self.mp_drawing_styles.get_default_hand_connections_style()
                for style in connections_style.values():
                    style.color = (128, 64, 128)
                
                # draw landmarks on top of frame
                self.mp_drawing.draw_landmarks(
                    frame,
                    self.hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
            
        return frame

    def frame_transform(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        return frame

    # Wait for a user to initiate an input, returns when the user is about to give an input, runs on FSM
    def is_hand_in_frame(self, frame: npt.NDArray):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame)
        hand_in_frame = results.multi_hand_landmarks != None
        return hand_in_frame

    def wait_for_input(self):
        print("Waiting for user input")
        frame = streamer.frame
        while frame is None:
            frame = streamer.frame
            time.sleep(.1)
        
        stop_threads = False
        t1 = Thread(target=self.display_frame_wait_thread, args=(lambda : stop_threads, ))
        t1.start()

        while not self.is_hand_in_frame(frame):
            frame = streamer.frame
            turn_towards_pose(frame)

        stop_threads = True
        t1.join()       

    # Captures the full sign input from the user, utilizes more complicated FSM logic
    def capture_full_input(self):
        print("Capturing input")
        self.curr_letter = ''
        self.curr_input = ''
        self.input_finished = 0
        
        stop_threads = False
        t1 = Thread(target=self.display_frame_predict_thread, args=(lambda : stop_threads, ))
        t1.start()
        while not self.input_finished:
            self.parse_frame()
        
        stop_threads = True
        t1.join()

        return self.curr_input

    def teardown(self):
        streamer.camera.teardown()
