from PIL import ImageOps as io,ImageGrab as ig
import time,pyautogui as pag
from numpy import array

def refresh():
    pag.click(960,168)

def jump():
    pag.keyDown('space')
    time.sleep(0.05)                   
    pag.keyUp('space')

def crop():
    box=(747,168,830,168)
    img=ig.grab(box)
    gimg=io.grayscale(img)
    arr=array(gimg.getcolors())
    return arr.sum()

def over():
    box=(944,154,975,182)
    img=ig.grab(box)
    gimg=io.grayscale(img)
    arr=array(gimg.getcolors())
    return arr.sum()

refresh()
d={}
a=2000
while a:
    d[crop()]=1
    if crop()==3301:
        jump()
        jump()
      
    if over()==1198:
       break
    a-=1
print(d)