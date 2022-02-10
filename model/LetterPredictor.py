# imports
import numpy as np # linear algebra

from torchvision import transforms

import torch
from torch.nn import functional as F

import cv2

from ASLResNet18 import ASLResNet18

class LetterPredictor:
    def __init__(self, checkpoint_path, transforms):
        self.model = ASLResNet18.load_from_checkpoint(checkpoint_path, map_location=torch.device('cpu'))
        self.model.eval()
        self.transforms = transforms
        
    def predict(self, image: np.ndarray):
        # image: numpy array in BGR format
        image = self.transforms(image)
        image = torch.unsqueeze(image,0)
        
        logits = self.model(image)
        pred = torch.argmax(F.softmax(logits[:,0:4], dim=-1), dim=1)
        print(pred.item())
        name = chr(pred.item()+65) # ascii code for upper case A
        
        return name


if __name__ == "__main__":
    test_transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(size=(64,64)),
        transforms.ToTensor(),
    ])
    checkpoint_path = "./sample-asl-combodata.ckpt"
    image_path = "../data/a/a1.jpg"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    lp = LetterPredictor(checkpoint_path, test_transforms)
    print(lp.predict(image))