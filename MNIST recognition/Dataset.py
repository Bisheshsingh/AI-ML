from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt


class dataloader:
    def __init__(self,batch_size):
        self.transform=transforms.Compose([
            transforms.Resize((32,32)),
            transforms.ToTensor()
        ])
        
        self.train=datasets.MNIST(root='dataset/',train=True,transform=self.transform,download=True)
        self.train_load=DataLoader(dataset=self.train,batch_size=batch_size,shuffle=True)
        self.test=datasets.MNIST(root='dataset/',train=False,transform=self.transform,download=True)
        self.test_load=DataLoader(dataset=self.test,batch_size=batch_size,shuffle=True)
        
    def get_train_loader(self):
        return self.train_load
    
    def get_test_loader(self):
        return self.test_load

