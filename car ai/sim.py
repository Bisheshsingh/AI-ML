import sys
import math
import pygame,random,numpy as np,time

pygame.init()
kli=False
pygame.display.set_caption("SELF DRIVING CAR SIMULATOR")
WINDOW_SIZE = 1200,650
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
CAR_SIZE = 30, 51
CAR_CENTER = 116, 141
DELTA_DISTANCE = 10
DELTA_ANGLE = 30
WHITE_COLOR = (255, 255, 255, 255)
TRACK = pygame.image.load('C:/Users/Bishesh Singh/Desktop/CSE 202/Python/AI/car ai/track3.png').convert_alpha()
TRACK_COPY = TRACK.copy()
FONT = pygame.font.SysFont("bahnschrift", 25)
CLOCK = pygame.time.Clock()
GENERATION = 0

def point(p,ang,d):
    rad=math.radians(ang)
    x=p[0]+d*math.cos(rad)
    y=p[1]+d*math.sin(rad)
    return (x,y)

def distance(x,y):
    return int(math.sqrt((y[0]-x[0])**2+(y[1]-x[1])**2))

class Car:
    def __init__(self,q,epsilon,gamma,alpha):
        self.corners = []
        self.q=q
        self.edge_points = []
        self.edge_distances = []
        self.reward = 0
        self.angle = 0
        self.epsilon=epsilon
        self.gamma=gamma
        self.distance=DELTA_DISTANCE
        self.alpha=alpha
        self.moves=[-1,0,1,2,-2]
        self.move=None
        self.car_center = CAR_CENTER
        self.car = pygame.image.load("C:/Users/Bishesh Singh/Desktop/CSE 202/Python/AI/car ai/car2.png").convert_alpha()
        self.car = pygame.transform.scale(self.car, CAR_SIZE)
        self.crashed = False
        self.ups()

    def ups(self):
        angles=[390-self.angle,90-self.angle,150-self.angle,360-self.angle,180-self.angle]
        angles=[math.radians(i) for i in angles]
        edgep=[]
        edged=[]
        for ang in angles:
            d=0
            ex,ey=self.car_center
            ex=int(ex)
            ey=int(ey)
            while TRACK_COPY.get_at((ex,ey))!=WHITE_COLOR:
                ex=int(self.car_center[0]+d*math.cos(ang))
                ey=int(self.car_center[1]+d*math.sin(ang))
                d+=1
            edgep.append((ex,ey))
            edged.append(d)
        self.edge_points=edgep
        self.edge_distances=edged
    
    def dspedge(self):
        for point in self.edge_points:
            pygame.draw.line(SCREEN, (0, 255, 0), self.car_center, point)
            pygame.draw.circle(SCREEN, (0, 255, 0), point, 5)
            
    def get_q(self,data,move):
        val=data+(move,)
        try:
           return self.q[val]
        except:
            return 10

    def enc(self,data):
        val=()
        idx=max(data)
        for i in data:
            if i<60:
                val+=(1,)
            else:
                val+=(0,)
        return val

    def crash(self):
        for corner in self.corners:
            corner=(int(corner[0]),int(corner[1]))
            if TRACK.get_at(corner) == WHITE_COLOR:
                return True
        return False
    
    def display_car(self):
        rotated_car = pygame.transform.rotate(self.car, self.angle)
        rect = rotated_car.get_rect(center=self.car_center)
        SCREEN.blit(rotated_car, rect.topleft)

    def rewardassign(self,move,dist,reward):
        prev_q=self.get_q(dist,move)
        q_val=[self.get_q(dist,a) for a in self.moves]
        max_q_val=max(q_val)
        best_moves=[i for i in q_val if i==max_q_val]
        best_move=random.choice(best_moves)
        best=self.moves[q_val.index(best_move)]
        val=dist+(best,)
        self.q[val]=self.alpha*(reward+self.gamma*max_q_val)-prev_q


    def upp(self):
        if random.random()<self.epsilon and not kli:
            self.move=random.choice(self.moves)
        else:
            q_val=[self.get_q(self.enc(self.edge_distances),a) for a in self.moves]
            max_q_val=max(q_val)
            best_moves=[i for i in q_val if i==max_q_val]
            best_move=random.choice(best_moves)
            self.move=self.moves[q_val.index(best_move)]
        
        #self.move=my_val[self.enc(self.edge_distances)]
        if self.move==-1:
            self.angle+=DELTA_ANGLE
        elif self.move==1:
            self.angle-=DELTA_ANGLE
        elif self.move==2:
            if self.distance+0.5:
               self.distance+=0.5
        elif self.move==-2:
            if self.distance-0.5>10:
               self.distance-=0.5
        
        self.rewardassign(self.move,self.enc(self.edge_distances),10)

        self.car_center = point(self.car_center,90-self.angle, self.distance)
        dist = math.sqrt(CAR_SIZE[0]**2 + CAR_SIZE[1]**2)/2
        corners = []
        corners.append(point(
            self.car_center, 60 - self.angle, dist))
        corners.append(point(
            self.car_center, 120 - self.angle, dist))
        corners.append(point(
            self.car_center, 240 - self.angle, dist))
        corners.append(point(
            self.car_center, 300 - self.angle, dist))
        self.corners = corners
        return (self.move,self.enc(self.edge_distances))

q={}
my_val={(1,0,1):0,(0,0,0):0,(1,0,0):1,(0,0,1):-1,(0,1,1):-1,(1,1,0):1,(0,1,0):-1}

def play(q_list):  
    cars=[Car(i,0.45,0.9,0.3) for i in q_list]
    new_cars=[]
    no_cars=len(cars)
    while no_cars:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        SCREEN.blit(TRACK, (0, 0))
        max_speed=0
        for i in cars:
            tp=i.upp()
            i.display_car()
            i.ups()

            if i.crash():
               i.rewardassign(tp[0],tp[1],-10)
               new_cars.append(i.q)
               cars.remove(i)
               no_cars-=1
            max_speed=max(max_speed,i.distance)
            #i.dspedge()
        msg = "Generation: {} Cars: {}  MaxSpeed: {}".format(GENERATION,no_cars,max_speed/0.5)
        text = FONT.render(msg, True, (0, 0, 0))
        SCREEN.blit(text, (0, 0))
        pygame.display.update()
        CLOCK.tick(50)
    return new_cars

q_l=[q for i in range(100)]
for i in range(200):
    GENERATION+=1
    if GENERATION%4==0:
        print('sbjk')
        kli=True
    else:
        kli=False
    q_l=play(q_l)
    