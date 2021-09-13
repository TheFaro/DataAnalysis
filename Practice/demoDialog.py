#create a bar of simple buttons that launch dialog demos

from Tkinter import *
from dialogTable import *
from quitter import Quitter

class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init(self, parent, **options)
        self.pack()
        Label(self, text='Basic demos').pack()
        for (key, value) in demos.items():
            Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)


if __name__ == '__main__': Demo().mainloop()