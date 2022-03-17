import Utils

class Train:
    def __init__(self,model,train_load,criterion,optimizer,device,printval=True):
        self.model=model
        self.train_load=train_load
        self.criterion=criterion
        self.optimizer=optimizer
        self.device=device
        self.printval=printval
    
    
    def training(self,epochs):
        for i in range(epochs):
            self.train_model(i+1)
        return self.model
        
    def train_model(self,epoch):
        num_correct=0
        num_samples=0
        for batch_idx,(data,outputs) in enumerate(self.train_load):
            data=data.to(self.device)
            outputs=outputs.to(self.device)
            #data=data.reshape(data.shape[0],-1)

            scores=self.model(data)
            loss=self.criterion(scores,outputs)
        
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            _,pred=scores.max(1)
            num_correct+=(pred==outputs).sum()
            num_samples+=pred.size(0)
            Utils.printProgressBar(num_samples, 60000, prefix = 'Progress:', suffix = 'Complete', length = 20)
       
        ret=(float(num_correct/num_samples)*100,int(num_correct),int(num_samples))
        if self.printval:
           Utils.print_accuracy(ret, 'Epoch-> '+str(epoch)) 
        else:
            pass
            
        
    

