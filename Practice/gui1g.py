from Tkinter import *

root = Tk()

widget = Label(root)
widget.config(text='Hello GUI World!')
widget.pack(expand=YES,fill=BOTH)
root.title('gui.py')
root.mainloop()