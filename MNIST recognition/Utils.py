import torch,time
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import pickle as pck
from Description import description

def Accuracy(loader,model,device,printval=True):
    num_correct=0
    num_samples=0
    model.eval()
    with torch.no_grad():
        for x,y in loader:
            x=x.to(device)
            y=y.to(device)
            #x=x.reshape(x.shape[0],-1)
            scores=model(x)
            _,pred=scores.max(1)
            num_correct+=(pred==y).sum()
            num_samples+=pred.size(0)
            printProgressBar(num_samples, 10000, prefix = 'Progress:', suffix = 'Complete', length = 20)

    model.train()
    ret=(float(num_correct/num_samples)*100,int(num_correct),int(num_samples))
    if printval:
        print_accuracy(ret, 'Training' if loader.dataset.train else 'Test')
    return ret

def save_model(model,acc,path=description['save models']):
    name=description['project name']+'-'+model.__class__.__name__+'-'+str(int(acc))
    file=open(path+name,'wb')
    pck.dump(model, file)
    
def load_model(name,path=description['save models']):
    file=open(path+description['project name']+'-'+name,'rb')
    return pck.load(file)

def print_accuracy(tup,name):
    print('-------------------------------')
    print(name)
    print('Correct predictions:',tup[1])
    print('Total samples:',tup[2])
    print('Accuracy:',"{:.2f}".format(tup[0]))
    print('-------------------------------')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

