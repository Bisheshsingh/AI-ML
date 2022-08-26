import torch
import torch.nn as nn
import torch.nn.functional as F

class NN(nn.Module):
    def __init__(self,inp_size,classes):
        super(NN,self).__init__()
        self.l1=nn.Linear(inp_size,8)
        self.l2=nn.Linear(8,4)
        self.l3=nn.Linear(4,classes)
    
    def forward(self,x):
        o=F.relu(self.l1(x))
        o=F.relu(self.l2(o))
        o=self.l3(o)
        return o
    
    def get_weights(self):
        return [self.l1.weight,self.l2.weight,self.l3.weight]

    def set_weights(self,lw):
        with torch.no_grad():
            self.l1.weight=nn.Parameter(lw[0])
            self.l2.weight=nn.Parameter(lw[1])
            self.l3.weight=nn.Parameter(lw[2])