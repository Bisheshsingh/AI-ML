import torch.nn as nn
import torch
import torch.nn.functional as F


class NN(nn.Module):
    def __init__(self,inp_size,classes):
        super(NN, self).__init__()
        self.l1=nn.Linear(inp_size, 48)
        self.l2=nn.Linear(48, 24)
        self.l3=nn.Linear(24, 48)
        self.l4=nn.Linear(48, classes)
        
    def forward(self,x):
        o=F.relu(self.l1(x))
        o=F.relu(self.l2(o))
        o=F.relu(self.l3(o))
        o=self.l4(o)
        return o
    
class CNN(nn.Module):
    def __init__(self,in_channels,classes):
        super(CNN,self).__init__()
        self.cl1=nn.Conv2d(in_channels=in_channels, 
                           out_channels=8,kernel_size=(3,3),stride=(1,1),padding=(1,1))
        self.pl1=nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.cl2=nn.Conv2d(in_channels=8, out_channels=16, 
                           kernel_size=(3,3),stride=(1,1),padding=(1,1))
        self.pl2=nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.l3=nn.Linear(16*7*7, classes)
        
    def forward(self,x):
        o=F.relu(self.cl1(x))
        o=self.pl1(o)
        o=F.relu(self.cl2(o))
        o=self.pl2(o)
        o=o.reshape(o.shape[0],-1)
        return self.l3(o)
    
class ECNN(nn.Module):
    def __init__(self,in_channels,classes):
        super(ECNN,self).__init__()
        self.cl1=nn.Conv2d(in_channels=in_channels, 
                           out_channels=8,kernel_size=(3,3),stride=(1,1),padding=(1,1))
        self.pl1=nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.cl2=nn.Conv2d(in_channels=8, out_channels=16, 
                           kernel_size=(3,3),stride=(1,1),padding=(1,1))
        self.pl2=nn.MaxPool2d(kernel_size=(2,2),stride=(2,2))
        self.l3=nn.Linear(16*7*7, 64)
        self.l4=nn.Linear(64,48)
        self.l5=nn.Linear(48,classes)
        
    def forward(self,x):
        o=F.relu(self.cl1(x))
        o=self.pl1(o)
        o=F.relu(self.cl2(o))
        o=self.pl2(o)
        o=o.reshape(o.shape[0],-1)
        o=F.relu(self.l3(o))
        o=F.relu(self.l4(o))
        return self.l5(o)
        
class LeNet(nn.Module):
    def __init__(self,in_channels,classes):
        super(LeNet,self).__init__()
        self.cl1=nn.Conv2d(in_channels=in_channels,out_channels=6,
                           kernel_size=(5,5),stride=(1,1),padding=(0,0))
        self.pl1=nn.AvgPool2d(kernel_size=(2,2),stride=(2,2))
        
        self.cl2=nn.Conv2d(in_channels=6,out_channels=16,
                           kernel_size=(5,5),stride=(1,1),padding=(0,0))
        self.pl2=nn.AvgPool2d(kernel_size=(2,2),stride=(2,2))
        
        self.cl3=nn.Conv2d(in_channels=16,out_channels=120,
                           kernel_size=(5,5),stride=(1,1),padding=(0,0))
        
        self.l4=nn.Linear(120, 84)
        self.l5=nn.Linear(84,10)
        
        
    def forward(self,x):
        o=F.relu(self.cl1(x))
        o=self.pl1(o)
        o=F.relu(self.cl2(o))
        o=self.pl2(o)
        o=F.relu(self.cl3(o))
        o=o.reshape(o.shape[0],-1)
        o=F.relu(self.l4(o))
        return self.l5(o)
        
        

        
        
        