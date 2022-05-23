import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(script_dir, '..', 'common'))
# sys.path.append('pose_tracker/project_posenet')
sys.path.insert(0, '/home/pi/MANI/interpreter/project-posenet')

import mediapipe as mp
import time

# from project_posenet import pose_engine
# from pose_engine import PoseEngine

# engine = PoseEngine(
#     'project-posenet/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
from simple_pose import engine


from PIL import Image
from PIL import ImageDraw

import numpy as np
import os


try:
    from rpi_hardware_pwm import HardwarePWM
    from time import sleep

    pwm = HardwarePWM(pwm_channel=1, hz=50)
    pwm.start(100) # full duty cycle
    SLEEP_TIME = .03
    MAX = 180
    RPI_CRASH = None
except Exception as e:
    print("FAILED TO INIT RPI LIBRARIES")
    RPI_CRASH = e


current_duty = 5

    
def turn_towards_pose(image):
    global current_duty
    pil_image = Image.fromarray(image)
    poses, inference_time = engine.DetectPosesInImage(pil_image)

    if poses:
        print(poses[0].keypoints[0].point)
        print(poses[0].keypoints[0].point.x)
        image_hight, image_width, _ = image.shape
        midpoint = image_width/2

        x_coodinate = poses[0].keypoints[0].point.x

        SPEED = 0.4
        print(x_coodinate,current_duty)
        print(midpoint)
        if abs(x_coodinate-midpoint) > 100:

            print("moving")
            if x_coodinate < midpoint:
                current_duty -= SPEED
                pwm.change_duty_cycle(current_duty)


            if x_coodinate > midpoint:
                current_duty += SPEED
                pwm.change_duty_cycle(current_duty)


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


    pwm.change_duty_cycle(50)


    for i in range(0,180):

        pwm.change_duty_cycle(percent_to_duty(i))
        sleep(SLEEP_TIME)

    for i in range(MAX,0,-1):
        pwm.change_duty_cycle(percent_to_duty(i))
        sleep(SLEEP_TIME)

    # pwm.change_frequency(25_000)

    pwm.stop()
