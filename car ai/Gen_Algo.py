import numpy as np
import random,torch
from NN import NN

class GA:
    def __init__(self,count,mut_rate):
        self.count=count
        self.mut_rate=mut_rate
    
    def evaluate(self,population):
        best_ai=None
        best_score=0

        sec_best_ai=None
        sec_best_score=0

        for ind in population:
            if self.fitness(ind)>best_score:
                sec_best_ai=best_ai
                sec_best_score=best_score
                best_ai=ind.ai
                best_score=ind.reward
        
        for i in range(self.count):
            population[i].ai=self.reproduction(population[i].ai,best_ai)
            population[i].restart()
        
        return population

    def fitness(self,obj):
        return obj.reward
    
    def crossover_and_mutation(self,parentA,parentB):
        child=NN(6,3).to('cpu')
        ch_wgt=child.get_weights()
        mutation=random.randint(-self.mut_rate,self.mut_rate)/100
        with torch.no_grad():
            for layer in range(len(ch_wgt)):
                for i in range(ch_wgt[layer].shape[0]):
                    for j in range(ch_wgt[layer].shape[1]):
                        x=random.randint(0,1)
                        if x==1:
                           ch_wgt[layer][i][j]=parentA[layer][i][j]+mutation
                        else:
                           ch_wgt[layer][i][j]=parentB[layer][i][j]+mutation
        child.set_weights(ch_wgt)
        return child
    
    def reproduction(self,parentA,parentB):
        aw,bw=parentA.get_weights(),parentB.get_weights()
        return self.crossover_and_mutation(aw,bw)

