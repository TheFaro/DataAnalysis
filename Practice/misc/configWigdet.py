import Tkinter 
from Tkinter import *

root = Tk()
labelfont = ('times', 24, 'italic')

widget = Label(root, text='Eat At Joes')
widget.config(bg='black', fg='red')

widget.pack(expand=YES, fill=BOTH)
root.mainloop()
