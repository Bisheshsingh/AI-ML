import random,math
import numpy as np
import pygame,sys,time
from NN import NN
from Genetic_Algorithm import GA

pygame.init()
pygame.display.set_caption("Evolution")
WINDOW_SIZE = 1280,650
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
FONT = pygame.font.SysFont("bahnschrift", 25)
CLOCK = pygame.time.Clock()
TRACK = pygame.image.load('C:/Users/Bishesh Singh/Desktop/CSE 202/Python/AI/car ai/track4.png').convert_alpha()
DISTANCE=10

def text(msg,x=0,y=0):
    text = FONT.render(msg, True, (0, 0, 0))
    SCREEN.blit(text, (x, y))

def point(p,ang,d):
    rad=math.radians(ang)
    x=p[0]+d*math.cos(rad)
    y=p[1]+d*math.sin(rad)
    return (x,y)

class Tiboid:
    def __init__(self):
        self.tiboid=pygame.image.load('C:/Users/Bishesh Singh/Desktop/CSE 202/Python/AI/car ai/spec.png').convert_alpha()
        self.tiboid= pygame.transform.scale(self.tiboid, (15,25))
        self.distance=DISTANCE
        self.angle=90
        self.score=0
        self.center=(random.randint(100,1000),random.randint(100,500))
        self.inp_size=5
        self.ai=NN(5,8)
        self.ai.add(NN(8,16))
        self.ai.add(NN(16,3))
        self.angles=[[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    
    def display(self):
        rotated_car = pygame.transform.rotate(self.tiboid, self.angle)
        rect = rotated_car.get_rect(center=self.center)
        SCREEN.blit(rotated_car, rect.topleft)
    
    def brain(self):
        inp=[self.center[0]/1280,self.center[1]/650]
        val=self.angle/45
        inp.extend(self.angles[int(val-1)])
        angle_arr=self.ai.predict(inp)
        new_angle_arr=[]
        for i in angle_arr:
            if i[0]>0.5:
                new_angle_arr.append(1)
            else:
                new_angle_arr.append(0)
        idx=self.angles.index(new_angle_arr)
        angle=(idx+1)*45

        return angle

    def update(self):
        self.angle=self.brain()
        self.center=point(self.center,270-self.angle,self.distance)
        self.score+=1
        return self

    def dead(self):
        if self.center[0]<10 or self.center[0]>1280:
           return True
        if self.center[1]<10 or self.center[1]>650:
            return True
        return False
    
    def getScore(self):
        return self.score
    
    def get(self):
        return self.ai
    
    def set(self,ai):
        self.ai=ai

def play(tiboids,max_score,gen):
    next_tiboid=[]
    score=0
    t=50
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
        key_input = pygame.key.get_pressed()   
        if key_input[pygame.K_LEFT] or score>200:
            next_tiboid.extend(tiboids)
            break
        if gen%5==0:
            t=30
        else:
            t=500
        SCREEN.blit(TRACK, (0, 0))

        for i in tiboids:
            i.display()
            i.update()
            max_score=max(i.getScore(),max_score)
            score=max(i.getScore(),score)
            if i.dead():
               next_tiboid.append(i)
               tiboids.pop(tiboids.index(i))
        text('Tiboids : '+str(len(tiboids)))
        text('Generation : '+str(gen),y=60)
        text('Max Score : '+str(max_score),y=20)
        text('Score : '+str(score),y=40)
        pygame.display.update()
        if len(tiboids)==0:
           break
        CLOCK.tick(t)
    return next_tiboid,max_score

next_Generation=[Tiboid() for i in range(500)]
ga=GA()
score=0
generation=0
while True:
    cGeneration,score=play(next_Generation,score,generation)
    next_Generation=ga.simulate(cGeneration)
    generation+=1

