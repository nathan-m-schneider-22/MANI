# rate and buffer parameters
TIME_PER_SIGN = 1 # must hold sign for TIME_PER_SIGN seconds before recognizes
INITIAL_TIME = .1
MAX_BUFFER_SIZE = 40
MIN_BUFFER_SIZE = 3
TIME_LOOKBACK = 10

# display thread
THREADING = 0

# mediapipe hyperparameters
MODEL_COMPLEXITY = 0
MIN_DETECTION_CONFIDENCE = .8
MIN_TRACKING_CONFIDENCE = .6

# sequence model parameters
SEQUENCE_INPUT_SIZE = 5 # nubmer of frames
WORD_WEIGHT = .7

import os
try:
    RPI_DETECTED = os.uname()[0] == "Linux"
except:
    RPI_DETECTED = False