import tkinter as tk
import xlrd

from select_file_frame import *
from select_cells_frame import *

class SelectSheet(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        #class variables
        self.mBook = xlrd.open_workbook(master.mFilePath)   #hold the recently opened workbook
        self.BookList = self.mBook.sheets()    

        #loop that builds the buttons to display the sheet names
        for i in range(0, len(self.mBook.sheets())) :
            Button = tk.Button(self,text=self.BookList[i].name,command=lambda i=i: self.buttonClick(master,i))
            Button.pack()

        #defining a back button
        tk.Button(self,text='Back',command=lambda: self.goBack(master),fg='white',bg='black').pack(pady=20)
    
    def goBack(self,master):
        from select_file_frame import SelectFileFrame
        master.switch_frame(SelectFileFrame)

    #function to handle button click
    def buttonClick(self, master,index):
        if index != None:
            self.chosenName(master,self.BookList[index])
        else: 
            print("There is an error")

    def chosenName(self, master, name):
        master.setChosenSheet(name)
        print(master.mChosenSheet.name)
        master.switch_frame(SelectCellsFrame)
    
    def __call__(self, master):
        SelectSheet(master).pack()
