import os

description={
    'project name' : 'Hand_written_digit_classification',
    'save models' : os.getcwd()+ '/SavedModels/',
    'project dir' : os.getcwd(),
    'custom images' : os.getcwd()+ '/Custom/',
}

requrements=[
    'torch',
    'torchvision',
    'pickles',
    'numpy',
    'pillow'
]

def allImports():
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    from torch.utils.data import DataLoader
    import torchvision.datasets as datasets
    import torchvision.transforms as transforms
    import pickle as pck