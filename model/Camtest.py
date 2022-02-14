import random
import os
import getpass
import cv2
#import Letter Predictor model 

#Dummy model selects random letter  - use real model later 
def dummy_predict(image):
    #pass image to model 
    rndlet = ['A','B','C','D','E','F','G','H','I','J','K','M']
    i = random.randint(0,len(rndlet)-1)
    return rndlet[i]

def make_directory(path):
    os.mkdir(path) 
    print("Made directory at "  + path)
    

def take_pic(path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    else:
        print("opening camera")
        
    while(True):
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        
        #Hit space when ready to capture image
        if k%256 == 32:
            print("Space hit, capturing image")
            image_path = path + "/image.jpeg"
            cv2.imwrite(image_path, frame)
            print(dummy_predict(image_path)) #pass to Letter Predictor model
            
        #Hit escape to quit camera 
        if k%256 == 27:
            print("Escape hit, closing...")
            break

    cap.release()
    cv2.destroyAllWindows()


#----------------------------------------------


path = "/Users/sarahkorb/Downloads/ManiImage" #edit this

if __name__ == "__main__":
    make_directory(path)
    take_pic(path)

