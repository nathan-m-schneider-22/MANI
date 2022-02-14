import random
import os
import getpass
import cv2
import numpy as np
# import Letter Predictor model
from LetterPredictor import LetterPredictor

# Dummy model selects random letter


def dummy_predict(image):
    # pass image to model
    rndlet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M']
    i = random.randint(0, len(rndlet)-1)
    return rndlet[i]


def make_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        print("Made directory at " + path)
    else:
        print("Directory " + path + " already exists, will place images here...")


def take_pic(path, model):
    num = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    else:
        print("opening camera")

    while(True):  # continuous picture taking
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        #image_path = path + "/image" + str(num) + ".jpg"
        #cv2.imwrite(image_path, frame)
        exit(1)

        print(model.predict(frame))  # pass to Letter Predictor model
        num += 1

        # Hit escape to quit camera
        if k % 256 == 27:
            print("Escape hit, closing...")
            break

    cap.release()
    cv2.destroyAllWindows()


# ----------------------------------------------

getUser = getpass.getuser()
path = "/Users/" + getUser + "/Downloads/ManiImage"

if __name__ == "__main__":
    checkpoint_path = "./sample-asl-combodata.ckpt"
    lp = LetterPredictor(checkpoint_path)
    make_directory(path)
    take_pic(path, lp)
