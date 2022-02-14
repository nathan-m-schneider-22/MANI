=======
# README

Run an ASL classification model using continuous images captured from a webcam.

# Files

ASLResNet18.py : Model Class

LetterPredictor.py: Loads the model and makes a prediction

CamTest.py: Takes continuous photos from webcam and feeds them to model. *Note* dummy model function is currently used; for actual classification, import and load the pre-trained model

sample-asl-combodata.ckpt: Pre-trained model

### Usage 
To classify a pre-saved image, run LetterPredictor.py. 


# Model setup
Dependencies include:
- cv2 (opencv) 
- torch (pytorch)
- torchvision
- pytorchlightning
- torchmetrics
- numpy 
- pandas


Highly recommend using a conda enviro to install dependencies. 