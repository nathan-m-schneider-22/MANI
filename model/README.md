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

# Running Model 
To test model with camera, cd into the model folder and then run python Camtest.py. I setup the softmax to just max over a, b, c so that it works for the demo. If it doesn't seem to be working, try moving hand closer to camera. 