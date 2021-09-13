from Tkinter import *
import tkMessageBox
import Tkinter

top = Tkinter.Tk()

def helloCallBack():
    tkMessageBox.showinfo("Hello Python", "Hello World")

B = Tkinter.Button(top, text="Hello", command=helloCallBack)
B.pack()
B.place(height=50,width=50)
top.mainloop()