from tkinter import *
states = []

def check(i):

	if True in states:
		print("Cannot add another one")
	else:
		states[i] = not states[i]
		print(states)



root = Tk()

for i in range(4):
	test = Checkbutton(root, text=str(i), command=(lambda i=i: check(i)) )
	test.pack(side=TOP)
	states.append(0)

root.mainloop()

print(states)
