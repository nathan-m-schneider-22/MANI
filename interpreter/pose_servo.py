import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(script_dir, '..', 'common'))
sys.path.insert(0, '/home/pi/MANI/interpreter/project-posenet')

import mediapipe as mp
import time
from simple_pose import engine
from PIL import Image, ImageDraw
import numpy as np
from time import sleep
import cv2
from rpi_hardware_pwm import HardwarePWM


pwm = HardwarePWM(pwm_channel=1, hz=50)
pwm.start(100) # full duty cycle
SLEEP_TIME = .03
MAX = 180
current_duty = 10
DUTY_MIN = 7
DUTY_MAX = 11
    
def get_hip_shoulder_dist(pose):
    
    dist1 = pose.keypoints[5].point.y - pose.keypoints[11].point.y 
    dist2 = pose.keypoints[6].point.y - pose.keypoints[12].point.y 

    return -(dist1 + dist2) / 2



def turn_towards_pose(image):
    global current_duty
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(image)
    poses, inference_time = engine.DetectPosesInImage(pil_image)

    # for p in poses:
    #     print(get_hip_shoulder_dist(p))

    print("current duty: ",current_duty)

    if poses:

        pose = max(poses, key=get_hip_shoulder_dist)
        image_hight, image_width, _ = 480, 640, 0

        midpoint = image_width/2

        x_coodinate = pose.keypoints[0].point.x

        SPEED = 0.2
        # print(x_coodinate-midpoint,current_duty)
        if abs(x_coodinate-midpoint) > image_width/6:


            if x_coodinate < midpoint:
                current_duty = max(current_duty - SPEED, DUTY_MIN)
                pwm.change_duty_cycle(current_duty)


            if x_coodinate > midpoint:

                current_duty = min(current_duty + SPEED, DUTY_MAX)
                pwm.change_duty_cycle(current_duty)
        
        hand_level = min(pose.keypoints[9].point.y,pose.keypoints[10].point.y)
        shoulder_level = min(pose.keypoints[5].point.y,pose.keypoints[6].point.y)


        # for label, keypoint in pose.keypoints.items():
        #     print('  %-20s x=%-4d y=%-4d score=%.1f' %
        #         (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))

        # print(hand_level,shoulder_level)
        if hand_level < shoulder_level:
            print("RAISING HAND")
            return True
        
        return False


def percent_to_duty(angle):
    # return 
    duty = 3+ angle/180*8

    print(angle,":",duty)
    return float(duty)


if __name__ == "__main__":

    pwm = HardwarePWM(pwm_channel=1, hz=50)
    pwm.start(100) # full duty cycle
    SLEEP_TIME = .03
    MAX = 180
    INC = 5
    pwm.change_duty_cycle(50)

    for i in range(0,180,INC):
        pwm.change_duty_cycle(percent_to_duty(i))
        sleep(SLEEP_TIME)

    # for i in range(MAX,0,-1*INC,):
    #     pwm.change_duty_cycle(percent_to_duty(i))
    #     sleep(SLEEP_TIME)

    from picamera2 import Picamera2

    picam2 = Picamera2()
    # resolution = picam2.sensor_resolution
    resolution = (1280, 720 )

    picam2.configure(picam2.preview_configuration(main={"format": 'XRGB8888', "size": resolution}))
    picam2.start()


    cam = picam2
    while True:
        frame = cam.capture_array()
        image = cv2.flip(frame, 0)


        turn_towards_pose(image)
        # print(np.shape(frame))

        resize = cv2.resize(image, (620, 480))

        cv2.imshow("frame",resize)
        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for 1 millisecond
            break






    pwm.stop()



