import sys
import math
import pygame,torch,random
from NN import NN
from Gen_Algo import GA
import pickle as pck

class Car:
    def __init__(self,screen,car_center,car_size,car,track,ai=None):
        self.corners = []
        self.edge_points = []
        self.edge_distances = []
        self.track=track
        self.car_size=car_size
        self.track_cpy=track.copy()
        self.reward = 0
        self.angle = 360
        self.distance = random.randint(10,20)
        self.move=2
        self.screen=screen
        self.car_center=car_center
        self.car_center_cpy=car_center
        self.car = pygame.image.load(car).convert_alpha()
        self.car = pygame.transform.scale(self.car, self.car_size)
        self.crashed = False
        if ai==None:
           self.ai=NN(6,3).to('cpu')
        else:
           self.ai=ai
        self.ups()
        
    def point(self,p,ang,d):
        rad=math.radians(ang)
        x=p[0]+d*math.cos(rad)
        y=p[1]+d*math.sin(rad)
        return (x,y)

    def restart(self):
        self.corners = []
        self.edge_points = []
        self.edge_distances = []
        self.distance = random.randint(10,20)
        self.reward = 0
        self.angle = 0
        self.move=2
        self.car_center = self.car_center_cpy
        self.crashed = False
        self.ups()

    def ups(self):
        angles=[390-self.angle,90-self.angle,150-self.angle,360-self.angle,180-self.angle]
        angles=[math.radians(i) for i in angles]
        edgep=[]
        edged=[]
        white=(255, 255, 255, 255)
        for ang in angles:
            d=0
            ex,ey=self.car_center
            ex=int(ex)
            ey=int(ey)
            while self.track_cpy.get_at((ex,ey))!=white:
                ex=int(self.car_center[0]+d*math.cos(ang))
                ey=int(self.car_center[1]+d*math.sin(ang))
                d+=1
            edgep.append((ex,ey))
            edged.append(d)
        self.edge_points=edgep
        self.edge_distances=edged
    
    def dspedge(self):
        for point in self.edge_points:
            pygame.draw.line(self.screen, (0, 255, 0), self.car_center, point)
            pygame.draw.circle(self.screen, (0, 255, 0), point, 5)

    def crash(self):
        white=(255,255,255,255)
        for corner in self.corners:
            corner=(int(corner[0]),int(corner[1]))
            if self.track.get_at(corner) == white:
                return 1
        return 0

    def display_car(self):
        rotated_car = pygame.transform.rotate(self.car, self.angle)
        rect = rotated_car.get_rect(center=self.car_center)
        self.screen.blit(rotated_car, rect.topleft)

    def upp(self):
        self.move=self.brain()
        if self.move==1:
            self.angle+=30
        elif self.move==2:
            self.angle-=30

        self.car_center = self.point(self.car_center,90-self.angle, self.distance)
        dist = math.sqrt(self.car_size[0]**2 + self.car_size[1]**2)/2
        corners = []
        corners.append(self.point(
            self.car_center, 60 - self.angle, dist))
        corners.append(self.point(
            self.car_center, 120 - self.angle, dist))
        corners.append(self.point(
            self.car_center, 240 - self.angle, dist))
        corners.append(self.point(
            self.car_center, 300 - self.angle, dist))
        self.corners = corners

    def brain(self):
        feed=self.edge_distances[:]
        feed.append(self.distance)
        data=torch.Tensor(feed)
        output=int(self.ai(data).max(0)[1])
        return output

class Simulation:
    def __init__(self,track,gen,pop,mut,car,best=None):
        pygame.init()
        pygame.display.set_caption("SELF DRIVING CAR SIMULATOR")
        self.window_size = 1200,650
        self.root = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.SysFont("bahnschrift", 25)
        self.clock = pygame.time.Clock()
        self.GENERATION = 0
        self.GENERATIONS=gen
        self.POPULATION = pop
        self.best=best
        self.q=False
        self.Gen_Algo=GA(self.POPULATION,mut)
        self.track=pygame.image.load(track.get()).convert_alpha()
        self.cars=[Car(car_center=track.get_start(),screen=self.root,car=car,track=self.track,car_size=(30,51),ai=best) for i in range(self.POPULATION)]
    
    def play(self):  
        count=self.POPULATION
        new_cars=[]
        while count>0 and not self.q:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            key_input = pygame.key.get_pressed()   
            if key_input[pygame.K_r]:
                new_cars.extend(self.cars)
                break
            
            if key_input[pygame.K_s]:
                 new_cars.extend(self.cars)
                 best_ai=None
                 mx=0
                 for i in self.cars:
                    if i.reward>mx:
                        mx=i.reward
                        best_ai=i.ai
                 pck.dump(best_ai,open('saves/model1','wb'))
                 break
    
            self.root.blit(self.track, (0, 0))
            
            max_points=0
            for ind in self.cars:
                ind.ups()
                ind.dspedge()
                ind.display_car()
                if ind.distance>0:
                   ind.reward+=(ind.distance/2)
                ind.upp()
                if ind.crash():
                   count-=1
                   new_cars.append(ind)
                   self.cars.remove(ind)
                   #cars[i].restart()
                max_points=max(max_points,ind.reward)
        
            msg = "Generation: {} Popultion: {} Max points: {}".format(self.GENERATION,count,max_points)
            text = self.font.render(msg, True, (0, 0, 0))
            self.root.blit(text, (0, 0))
            pygame.display.update()
            self.clock.tick(30)
        self.cars=new_cars
    
    def simulate(self):
        for i in range(self.GENERATIONS):
            self.play()
            self.cars=self.Gen_Algo.evaluate(self.cars)
            self.GENERATION+=1
            if(self.q):
                return
        pygame.quit()
