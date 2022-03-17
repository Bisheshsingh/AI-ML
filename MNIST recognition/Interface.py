from tkinter import *
import tkcap
from Description import description
import matplotlib.pyplot as plt
from PIL import Image,ImageOps
import Utils,numpy,torch

class custominput:
    def __init__(self,model_name):
        self.models={'CNN' : 'CNN-98',
                     'NN' :  'NN-97',
                     'ECNN' : 'ECNN-99',
                     'LeNet' : 'LeNet-99'
                    }
        self.model=Utils.load_model(self.models[model_name])
        self.model_name=model_name
        self.res=28 if self.model_name!='LeNet' else 32
    
    def show(self,img):
        plt.imshow(img)
        
    def predict(self,data,show_plot=False):
        visual=['CNN','LeNet','ECNN']
        if show_plot:
           self.show(data[0])
        if self.model_name in visual:
           data=data.reshape((1,1,self.res,self.res))
        elif self.model_name=='NN':
           data=data.reshape((1,784))
        return int(self.model(data).max(1)[1])
    
    def convert_from_loader(self,data,idx):
        return data(batch_size=64).train[idx]

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.title('INTERFACE')
        self.cap = tkcap.CAP(self.root) 
        self.brush_button = Button(self.root, text='Brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=0)
        Button(text="Predict", command=self.Predict).grid(row=2,column=0)
        self.pred=Label(text=0)
        self.pred.grid(row=2,column=1)
        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)
        self.models = ttk.Combobox(self.root,values=list(custominput('CNN').models.keys()),width=5)
        self.models.current(0)
        self.models.grid(row=0,column=1)     
        self.c = Canvas(bg='white', width=110, height=150)
        self.c.grid(row=1, columnspan=5)
        self.setup()
        self.root.mainloop()
            
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 20
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.brush_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        
    def Predict(self):
        img=self.cap.capture(imageFilename=description['custom images']+'towa.png')
        res=32 if self.models.get()=='LeNet' else 28
        img=img.resize((res,res))
        img=ImageOps.invert(img.convert('L'))
        data=numpy.asarray(img).reshape((1,res,res))
        data=data.astype('float32')
        data=torch.from_numpy(data)
        self.pred.config(text=str(custominput(self.models.get()).predict(data,1)))
        
            
    def use_brush(self):
        self.activate_button(self.brush_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = 15 if not self.eraser_on else 200
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


Paint()
