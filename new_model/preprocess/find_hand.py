

import cv2
import os
import mediapipe as mp
from math import inf
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

plt.ion()   # interactive mode
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def crop_image(min_x, max_x, min_y, max_y,image):
    crop_img = image[int(min_y):int(max_y), int(min_x):int(max_x)]
    return crop_img

def find_xy_range(hand_landmarks,image_path):
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape
    index = 0
    min_x = inf
    max_x = -inf
    min_y = inf
    max_y = -inf
    while(index < 21):
        check_x = hand_landmarks.landmark[index].x
        check_y = hand_landmarks.landmark[index].y
        if check_x < min_x:
            min_x = check_x
        if  check_y < min_y:
            min_y =  check_y
        if check_x > max_x:
            max_x = check_x
        if  check_y > max_y:
            max_y = check_y
        index += 1
    
    min_x = min_x*image_width - 28
    max_x = max_x*image_width + 28
    min_y = min_y*image_height - 28
    max_y = max_y*image_height + 28
    
    cropped_img = crop_image(min_x, max_x, min_y, max_y,image)
    return cropped_img



def find_hand(image):    
    with mp_hands.Hands(static_image_mode=True,max_num_hands=2,min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            cropped_image = find_xy_range(hand_landmarks,path)
    return cropped_image

      
