import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

from preprocess.feature_extractor import extract_features
from joblib import load

def add_text_to_image(image, text, org):
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 1
    
    # Using cv2.putText() method
    image = cv2.putText(image, text, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    return image


model_path = "./output/model.joblib"
model = load(model_path)

pred_buffer = np.ones(shape=(0,26))
state_buffer = np.ones(shape=(0,26))

time_buffer = []

pred = ""
alpha = .04
state = np.array([1/26 for _ in range(26)])
curr_letter = ""
curr_string = ""
curr_pred = ""

# For webcam input:
cap = cv2.VideoCapture(0)

start_time = time.time()

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # image 
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # making prediction 
        features, _ = extract_features([hand_landmarks], ['a'], input_type ='inference')
        preds = model.predict_proba(features)
        pred_buffer = np.vstack([pred_buffer, preds])
        state_buffer = np.vstack([state_buffer, state])
        time_buffer.append(time.time())
        state = state + alpha*(preds-state)
        curr_pred = model.classes_[np.argmax(state)]
        pred = model.classes_[np.argmax(state)]
        if pred == '_':
            pred = ' ' 
        if time.time()-start_time > 3 and np.max(state)>.35:
            if curr_letter != pred:
                curr_letter = pred
                if curr_letter == 'x':
                    curr_string = curr_string[:-1]
                    curr_letter = ''
                    start_time = time.time()
                else:
                    curr_string += pred

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        if curr_letter == 'q':
            state = np.array([1/26 for _ in range(26)])
            curr_letter = ""
            curr_string = ""
            start_time = time.time()
            pred = 'clear'
    else:
        pred = 'no hand'
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)
    image = add_text_to_image(image, curr_pred, (0,50))
    image = add_text_to_image(image, curr_string, (0,400))
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()