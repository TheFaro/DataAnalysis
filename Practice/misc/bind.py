from Tkinter import *
 
root = Tk()
widget = Button(root, text='Hello world Event')
widget.pack()
widget.bind('<Enter>', lambda : (changeBackground(widget)))
widget.bind('<Double-1>',quit)


def changeBackground(widget):
    widget.config(bg='green')

root.mainloop()