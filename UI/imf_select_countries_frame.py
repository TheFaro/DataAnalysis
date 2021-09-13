import tkinter as tk
from tkinter import ttk as TTK
import requests
import json


class SelectCountriesFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.count_var = tk.StringVar()
        
        try:
            if len(master.IMF_var[1]['country']) > 0:
                print(" I am first")
                self.select_list = master.IMF_var[1]['country']
                print(self.select_list)
            else:
                print("I am second")
                self.select_list = []
        except (KeyError,IndexError): 
            print('I am in error')
            self.select_list = []

        #show countries in combobox
        tk.Label(self,text='Select Countries from list below',font=('Arial Bold', 18)).pack(side=tk.TOP)
        self.countries = TTK.Combobox(self,width = 27,textvariable=self.count_var)
        self.populateCombobox(master)
        self.countries.pack(side=tk.TOP)
        self.countries.current(0)
        self.createListbox(master)

        #create buttons
        tk.Button(self,text="Back",command=lambda:self.back(master)).pack(side=tk.TOP)
        tk.Button(self,text="Add Country to List",command=lambda:self.addToSelectedList(master)).pack(side=tk.TOP)
        tk.Button(self,text="Next",command=lambda:self.next(master)).pack(side=tk.TOP)
        
    def next(self,master):   
        from imf_select_indicators_frame import SelectIndicatorsFrame   
        if len(self.select_list) == 0:
            print("No country selected. Please select one.")
            mb.showinfo('No Country Selected. Please select at least one.')
        
        else:
            master.IMF_var.append({'country': self.select_list})
            master.switch_frame(SelectIndicatorsFrame)

    def back(self,master):
        from imf_select_frequency_frame import SelectFrequencyFrame
        master.switch_frame(SelectFrequencyFrame)

    def populateCombobox(self,master):
        temp = []

        for i,country in enumerate(master.country_list):
            temp.append(country['text'])

        self.countries['values'] = temp

    def addToSelectedList(self,master):
        for i,count in enumerate(master.country_list):
            if self.count_var.get() == count['text']:
                #add country code to selected list
                self.select_list.append(count)

                #add to listbox 
                self.addToListbox(i,count['text'])

    def createListbox(self,master):
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self,width="60",height="20")
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.listbox.pack(side=tk.LEFT,expand=tk.YES,fill=tk.X,pady=15)
        self.listbox.config(selectmode=tk.SINGLE,selectbackground='grey')
        self.listbox.bind('<Double-1>',self.deleteFromListbox)

        if len(self.select_list) > 0:
            for i,country in enumerate(self.select_list):
                self.listbox.insert(i,country['text'])

    def addToListbox(self, index, value):
        self.listbox.insert(index,value)

    def deleteFromListbox(self,event):
        print(self.select_list)
        idx = self.listbox.curselection()[0]
        #todo - use delete function to remove clicked item
        self.listbox.delete(idx)
        del self.select_list[idx]
        print(self.select_list)