import os
import sys
import time

script_dir = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(script_dir, '..', 'common'))
# sys.path.append('pose_tracker/project_posenet')
sys.path.insert(0, '/home/pi/MANI/interpreter/project-posenet')

import cv2
import mediapipe as mp
from argparse import ArgumentParser
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# from project_posenet import pose_engine
from pose_engine import PoseEngine

# engine = PoseEngine(
#     'project-posenet/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
from simple_pose import engine


from PIL import Image
from PIL import ImageDraw

import numpy as np
import os


from rpi_hardware_pwm import HardwarePWM
from time import sleep

pwm = HardwarePWM(pwm_channel=1, hz=50)
pwm.start(100) # full duty cycle
SLEEP_TIME = .03
MAX = 180



# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


def main(args):
    # video = init_video_stream_capture(args.video_source)
    current_duty = 5
    st = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        print((time.time() - st)*1000)
        st = time.time()
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = frame.array


        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(frame, 0), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False

        rawCapture.truncate(0)

        start_time = time.time()
        # results = pose.process(image)

        pil_image = Image.fromarray(image)
        poses, inference_time = engine.DetectPosesInImage(pil_image)

        end_time = (time.time() - start_time)*1000


        print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
        print("Time(ms): ", (time.time() - start_time)*1000) 

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if poses:
            print(poses[0].keypoints[0].point)
            print(poses[0].keypoints[0].point.x)
            image_hight, image_width, _ = image.shape
            midpoint = image_width/2

            x_coodinate = poses[0].keypoints[0].point.x

            SPEED = 0.5
            print(x_coodinate,current_duty)
            print(midpoint)
            if abs(x_coodinate-midpoint) > 50:

                print("moving")
                if x_coodinate < midpoint:
                    current_duty -= SPEED
                    pwm.change_duty_cycle(current_duty)


                if x_coodinate > midpoint:
                    current_duty += SPEED
                    pwm.change_duty_cycle(current_duty)


        cv2.imshow('MediaPipe Pose Estimation Demo', image)

        if cv2.waitKey(1) == 27:
            print('\nExit key activated. Closing video...')
            break

    video.release(), cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--video_source', type=int, default=0,
                        help='Device index to access video stream. Defaults to primary device camera at index 0')

    parser.add_argument('--min_detection_confidence', default=0.5, type=float,
                        help='Minimum confidence value ([0.0, 1.0]) from the face detection model for the detection to be considered successful. Default to 0.5')

    parser.add_argument('--model_complexity', default=0, type=int,
                        help='Landmark accuracy as well as inference latency generally go up with the model complexity. Default to 1')

    args = parser.parse_args()
    main(args)
