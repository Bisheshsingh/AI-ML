import numpy as np
import random
from NN import NN

class GA:

    def fitness(self,obj):
        return obj.getScore()
    
    def crossover_and_mutation(self,parentA,parentB):
        weight=[]
        w1=[]
        mut=0.05
        for i in range(len(parentA[0])):
            w=[]
            for j in range(len(parentB[0][i])):
                mutate=0
                if random.random()*2!=0:
                    mutate=mut
                if random.random()>0.5:
                    mutate=-mut
                choose=random.randint(0,1)
                if choose==1:
                    w.append(parentA[0][i][j]+mutate)
                else:
                    w.append(parentB[0][i][j]+mutate)
            w1.append(w)
        weight.append(np.array(w1))
    
        w3=[]
        for i in range(len(parentA[1])):
            w=[]
            for j in range(len(parentB[1][i])):
                mutate=0
                if random.random()*2!=0:
                   mutate=mut
                if random.random()>0.5:
                   mutate=-mut
                choose=random.randint(0,1)
                if choose==1:
                   w.append(parentA[1][i][j]+mutate)
                else:
                   w.append(parentA[1][i][j]+mutate)
            w3.append(w)
        weight.append(np.array(w3))

        w2=[]
        for i in range(len(parentA[2])):
            w=[]
            for j in range(len(parentB[2][i])):
                mutate=0
                if random.random()*2!=0:
                   mutate=mut
                if random.random()>0.5:
                   mutate=-mut
                choose=random.randint(0,1)
                if choose==1:
                   w.append(parentA[2][i][j]+mutate)
                else:
                   w.append(parentB[2][i][j]+mutate)
            w2.append(w)
        weight.append(np.array(w2))
        return weight
    
    def reproduction(self,parentA,parentB):
        parentA,parentB=parentA.get(),parentB.get()
        aw,bw=parentA.getWeights(),parentB.getWeights()
        child=NN(self.inp_size,8)
        child.add(NN(8,16))
        child.add(NN(16,3))
        child.setWeights(self.crossover_and_mutation(aw,bw))
        return child
    
    def simulate(self,population):
        self.population=population
        best_fitness=0
        bestidx=0
        secbestidx=0
        self.inp_size=population[0].inp_size
        for i in range(len(self.population)):
            cfitness=self.fitness(self.population[i])
            if cfitness>=best_fitness:
                best_fitness=cfitness
                secbestidx=bestidx
                bestidx=i

        idx=random.randint(0,len(self.population)-1)
        for i in range(len(self.population)):
            kl=random.randint(0,1)+1
            if kl:
               idx=random.randint(0,len(self.population)-1)
            else:
               idx=secbestidx
            new_child=self.reproduction(self.population[bestidx],self.population[idx])
            self.population[i].set(new_child)
            self.population[i].angle=90
            self.population[i].score=0
            #self.population[i].dinit=1-self.population[i].dinit
            #self.population[i].danger=1280*self.population[i].dinit-0
            self.population[i].center=(random.randint(100,1000),random.randint(100,500))
        return self.population
    