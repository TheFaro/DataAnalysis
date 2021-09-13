from Tkinter import *

def result( ):
	print 'The sum of 2+2 is =', 2+2

win = Frame()
win.pack( )
Label(win, text='Click Add to get the sum or Quit to Exit').pack(side=TOP)
Button(win, text='Add', command=result).pack(side=LEFT)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT)

win.mainloop( )
