import tkinter as tk

from select_file_frame import SelectFileFrame
from choose_data_source_frame import ChooseDataSourceFrame

class MenuFrame(tk.Frame):
    def __init__(self, master):
        #call the super class Frame constructor
        tk.Frame.__init__(self, master)

        #definition of frame widgets and their functionality
        #definition of the view charts button
        self.viewBtn = tk.Button(self,text='View Charts[Offline]',command=lambda: master.switch_frame(SelectFileFrame))
        self.viewBtn.pack(pady=20,ipadx=120,ipady=5)
        
        #definition of update data button
        self.updateBtn = tk.Button(self,text='View Charts[Online]',command=lambda:master.switch_frame(ChooseDataSourceFrame))
        self.updateBtn.pack(pady=20,ipadx=120,ipady=5)
        
        #definition of the exit button
        self.exitBtn = tk.Button(self,text='Exit',command=self.quit)
        self.exitBtn.pack(pady=12,ipadx=60,ipady=5)

