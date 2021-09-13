from Tkinter import *
from ttk import *

from tkFileDialog import *

root = Tk()
root.geometry('200x100')

def open_file():
    filename = askopenfilename(filetypes = (('Python Files', '*.py'),('All files', '*.*')))
    if filename is not None:
        #content = file.read()
        print(filename)


btn = Button(root, text='Open', command=lambda: open_file())
btn.pack(side=TOP, pady=10)

mainloop()