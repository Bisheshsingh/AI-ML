from Setup import setup
s=setup()

import torch.nn as nn
import torch.optim as optim
#custom
import Utils
from Model import NN,CNN,ECNN,LeNet
from Dataset import dataloader
from Training import Train
from Description import description


device='cpu'
inp_size=784
in_channels=1
classes=10 
learn_rate=1e-3
batch_size=64
epochs=1

model=LeNet(in_channels, classes)
#model=Utils.load_model('LeNet-99')
criterion=nn.CrossEntropyLoss()
optimizer=optim.Adam(model.parameters(),lr=learn_rate)

data_load=dataloader(batch_size)
train_model=Train(model, data_load.get_train_loader(), criterion, optimizer, device)

train_model.training(epochs)

test_acc=Utils.Accuracy(data_load.get_test_loader(), model, device)

#Utils.save_model(model,test_acc[0])























