# importing only those functions
# which are needed
from tkinter import *
from tkinter.ttk import *

# creating tkinter window
root = Tk()

# Adding widgets to the root window
Label(root, text = 'GeeksforGeeks', font =(
'Verdana', 15)).pack(side = TOP, pady = 10)

# Creating a photoimage object to use image
photo = PhotoImage(file = "Tracks/track.png")

# here, image option is used to
# set image on button
def fun():
     global img
     img=PhotoImage(file = "Tracks/track2.png")
     btn['image']=img
     root.after(1000, fun)

btn=Button(root, text = 'Click Me !', image = photo)
btn.pack(side = TOP)

fun()

mainloop()
