#define a name: callback demos table

from Tkinter import *
from Tkinter.filedialog import askopenfilename      #get standard dialogs
from Tkinter.colorchooser import askcolor           #they live in Lib/Tkinter
from Tkinter.messagebox import askquestion, showerror
from Tkinter.simpledialog import askfloat

demos = {
    'Open': askopenfilename,
    'Color' : askcolor,
    'Query':lambda: askquestion('Warning', 'You typed "rm*"\nConfirm?'),
    'Error':lambda: showerror('Error!', "He's dead, Jim"),
    'Input':lambda: askfloat('Entry', 'Enter credit card number')
}

class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init(self, parent, **options)
        self.pack()
        Label(self, text='Basic demos').pack()
        for (key, value) in demos.items():
            Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)


if __name__ == '__main__': Demo().mainloop()