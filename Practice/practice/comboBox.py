import tkinter as tk
from tkinter import ttk

#creating a tkinter window
window = tk.Tk()
window.title('ComboBox')
window.geometry('500x250')

#label text for title
ttk.Label(window, text='GFG Combobox Widget',
        background='green',foreground='white', font=("Times New Roman",15)).grid(row=0,column=1)

#label
ttk.Label(window,text='Select the Month: ',font=("Times New Roman",10)).grid(column=0,row=5,padx=10,pady=25)

#combo box creation
n = tk.StringVar()
monthChosen = ttk.Combobox(window, width=27,textvariable=n)

#adding combobox dropdown list
monthChosen['values'] = [' January',
                         ' February',
                         ' March',
                         ' April',
                         ' May',
                         ' June',
                         ' July',
                         ' August',
                         ' September',
                         ' October',
                         ' November',
                         ' December']

months = [
   {'name':' January','code':'01'},
   {'name':' February','code':'02'},
   {'name':' March','code':'03'},
   {'name':' April','code':'04'},
   {'name':' May','code':'05'},
   {'name':' June','code':'06'},
   {'name':' July','code':'07'},
   {'name':' August','code':'08'},
   {'name':' September','code':'09'},
   {'name':'October','code':'10'},
   {'name':'November','code':'11'},
   {'name':'December','code':'12'} 
]

monthChosen.grid(column=1,row=5)
monthChosen.current()
ttk.Button(window,text="Print selection",command=lambda:printThis()).grid(column=0,row=6)
ttk.Button(window,text="Add to List",command=lambda:addToList()).grid(column=1,row=6)
ttk.Button(window,text="Print List",command=lambda:printList()).grid(column=2,row=6)
selected_list = []

def printThis():
    print(n.get())

def addToList():

    for i,date in enumerate(months):
        if n.get() == date['name']:
            selected_list.append(date['code'])
    

def printList():
    print(selected_list)
window.mainloop()