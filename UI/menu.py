from tkinter import *
import tkinter.messagebox as mb

def comingSoon():
    mb.showinfo('Message', 'Implementation coming soon')

def makemenu(win):
    top = Menu(win)
    win.config(menu=top)

    file = Menu(top)
    file.add_command(label='New', command=comingSoon, underline=0)
    file.add_command(label='Open', command=comingSoon, underline=0)
    file.add_command(label='Save', command=comingSoon, underline=0)
    file.add_command(label='Quit', command=win.quit, underline=0)
    top.add_cascade(label='File', menu=file, underline=0)

    edit = Menu(top, tearoff=False)
    edit.add_command(label='Cut', command=comingSoon, underline=0)
    edit.add_command(label='Paste', command=comingSoon, underline=0)
    top.add_cascade(label='Edit',menu=edit, underline=0)