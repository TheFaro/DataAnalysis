import Tkinter as tk

root = tk.Tk()

for i in range(0,1):
        index.append(i)
                
def Function(event):
    if event == 1:
            print('The pressed button is 1')
    if event == 2:
            print('The pressed button is 2')

listOfButtons = []

Button = tk.Button(root,text='Button 1',command=lambda: Function(index[0]))
listOfButtons.append(Button)
Button.pack()

Button = tk.Button(root,text="Button 2", command=lambda : Function(index[1]))
listOfButtons.append(Button)
Button.pack()

root.mainloop()