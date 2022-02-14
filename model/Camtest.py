import random
import os
import getpass
import cv2
#import LetterPredictor

#Dummy model selects random letter 
def dummy_predict(image):
    #pass image to model 
    rndlet = ['A','B','C','D','E','F','G','H','I','J','K','M']
    i = random.randint(0,len(rndlet)-1)
    return rndlet[i]

def make_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path) 
        print("Made directory at "  + path)
    else:
        print("Directory "  + path + " already exists, will place images here...")
    

def take_pic(path, model_path):
#     test_transforms = transforms.Compose([
#     transforms.ToPILImage(),
#     transforms.Resize(size=(64,64)),
#     transforms.ToTensor(),
#     ])
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
        image_path = path + "/image" + str(num) + ".jpeg" #storing images 
        cv2.imwrite(image_path, frame)
        
#Using Real model:
#       image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#       lp = LetterPredictor(checkpoint_path, test_transforms)
#       print(lp.predict(image))
           
        print(dummy_predict(image_path)) #Dummy model
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
    make_directory(path)
    take_pic(path)

