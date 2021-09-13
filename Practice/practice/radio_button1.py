from tkinter import * 

master = Tk()
master.geometry("175x175")

v = StringVar()

#dictionary to create multiple buttons
values = {
    "RadioButton1" : "1",
    "RadioButton2" : "2", 
    "RadioButton3" : "3",
    "RadioButton4" : "4",
    "RadioButton5" : "5"
}


for (text,value) in values.items():
    Radiobutton(master,text = text, variable = v,command=lambda:printClicked(), value = value, indicator = 0, background= 'light blue').pack(fill=X,ipady=5)


def printClicked():
    print(v.get())

mainloop()  