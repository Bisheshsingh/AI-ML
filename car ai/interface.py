from tkinter import *
from PIL import ImageTk,Image
from sim_gen import Simulation,pck
import os
 
class Track:
    def __init__(self,name):
        self.path={'Level 1': 'Tracks/track.png',
                   'Level 2': 'Tracks/track2.png',
                   'Level 3': 'Tracks/track3.png',
                   'Level 4': 'Tracks/track4.png',
                   'Select_Level' : 'Tracks/track.png'
        }
        
        self.start={'Level 1': (199,278),
                    'Level 2': (68,354),
                    'Level 3': (118,162),
                    'Level 4': (132,203),
                    'Select_Level' : (199,278)
        }
        
        self.name=name;
    
    def get(self):
        return self.path[self.name]
    
    def get_start(self):
        return self.start[self.name]
    
class Interface:
    def __init__(self):
        self.root=Tk()
        self.root.geometry('400x400')
        self.logs=pck.load(open('Logs','rb'))
        
        background_image = ImageTk.PhotoImage(Image.open("background.png"))
        Label(self.root,image=background_image).pack(fill=BOTH, expand=YES)
        
        Label(self.root,text="SELF DRIVING CAR SIMULATOR",relief="solid",fg="blue",width=30,font=("arial",10,"bold")).place(x=70,y=10)
        self.root.title('SELF DRIVING CAR SIMULATOR')
        
        self.levels=['Level 1','Level 2','Level 3','Level 4']
        self.selected_level=StringVar(value=self.logs[0])
        
        def fun(event):
            global img
            img=self.resize(Track(self.selected_level.get()).get())
            self.img_1['image']=img
        
        self.select_level=OptionMenu(self.root, self.selected_level, *self.levels, command=fun)
        self.select_level.config(bg="orange")
        self.select_level.place(x=10,y=40)
        
        img=self.resize(Track(self.selected_level.get()).get())
        self.img_1=Label(self.root,image=img)
        self.img_1.place(x=220,y=40)
        
        Label(self.root,text="Generations : ",font=("arial",10,"bold"),bg="orange").place(x=10,y=80)
        self.sel_gen=IntVar(value=self.logs[1])
        self.generations=Spinbox(self.root, from_= 0, to = 1000,width=5,textvariable=self.sel_gen,bg="orange")
        self.generations.place(x=110,y=82) 
        
        Label(self.root,text="Population : ",font=("arial",10,"bold"),bg="orange").place(x=10,y=120)
        self.sel_pop=IntVar(value=self.logs[2])
        self.population=Spinbox(self.root, from_= 1, to = 100,width=5,textvariable=self.sel_pop,bg="orange")
        self.population.place(x=110,y=124) 
        
        Label(self.root,text="Mutation Rate : ",font=("arial",10,"bold"),bg="orange").place(x=10,y=160)
        self.sel_mut=IntVar(value=self.logs[3])
        self.mutation=Spinbox(self.root, from_= 1, to = 100,width=5,textvariable=self.sel_mut,bg="orange")
        self.mutation.place(x=120,y=164)
        
        Label(self.root,text="Model : ",font=("arial",10,"bold"),bg="orange").place(x=10,y=264)
        self.models=os.listdir('saves/')
        self.sel_save=StringVar(value='New')
        self.select_model=OptionMenu(self.root, self.sel_save, *self.models)
        self.select_model.config(bg="orange")
        self.select_model.place(x=80,y=260)
        
        self.start=Button(self.root,text="   Start   ",font=("arial",10,"bold"),bg='green',command=self.INITIALIZE)
        
        def onB2(event):
             self.start["bg"]="green2"

        def offB2(event):
            self.start["bg"]="green"
             
        self.start.bind('<Enter>',onB2)
        self.start.bind('<Leave>',offB2)
        self.start.place(x=170,y=330)
        
        self.cars=os.listdir('Cars/')
        self.sel_car=StringVar(value=self.logs[4])
        
        def fun1(event):
            global img1
            img1=self.resize1('Cars/'+self.sel_car.get())
            self.img_2['image']=img1
        
        self.select_car=OptionMenu(self.root, self.sel_car, *self.cars,command=fun1)
        self.select_car.config(font=("arial",10,"bold"),bg="orange")
        self.select_car.place(x=10,y=220)
        
        img1=self.resize1('Cars/'+self.logs[4])
        self.img_2=Label(self.root,image=img1)
        self.img_2.place(x=260,y=200)
        
        self.root.mainloop()
        
    def INITIALIZE(self):
        track=Track(self.selected_level.get())
        gen=self.sel_gen.get()
        pop=self.sel_pop.get()
        mut=self.sel_mut.get()
        if(self.sel_save.get()!='New'):
            best=pck.load(open('saves/'+self.sel_save.get(),'rb'))
        else:
            best=None
        
        self.logs=[self.selected_level.get(),gen,pop,mut,self.sel_car.get()]
        pck.dump(self.logs,open('Logs','wb'))
        
        Simulation(track=track,gen=gen,mut=mut,pop=pop,car='Cars/'+self.sel_car.get(),best=best).simulate()
    
    def resize(self,img):
        img=Image.open(img)
        img= img.resize((150,120), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    
    def resize1(self,img):
        img=Image.open(img)
        img= img.resize((70,100), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    
Interface()