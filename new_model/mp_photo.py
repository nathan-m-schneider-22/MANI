import random
import os
import getpass
import cv2
from joblib import load

from preprocess.feature_extractor import extract_features

def make_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path) 
        print("Made directory at "  + path)
    else:
        print("Directory "  + path + " already exists, will place images here...")
    

def take_pic(path, model):
    num = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    else:
        print("opening camera")
        
    while(True): #continuous picture taking
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        image_path = path + "/image" + str(num) + ".jpg"
        cv2.imwrite(image_path, frame)
        paths = [image_path]
        labels = ['a']
        features, labels = extract_features(paths, labels)
        if features.size > 0:
            print(model.predict(features)) #pass to Letter Predictor model
        else:
            print("no hand")
        num += 1
        
        #Hit escape to quit camera 
        if k%256 == 27:
            print("Escape hit, closing...")
            break

    cap.release()
    cv2.destroyAllWindows()


#----------------------------------------------

getUser = getpass.getuser()
path = "/Users/"  + getUser + "/Downloads/ManiImage"

if __name__ == "__main__":
    model_path = "./output/model.joblib"
    model = load(model_path)
    make_directory(path)
    take_pic(path, model)

