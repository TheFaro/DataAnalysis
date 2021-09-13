import tkinter as tk
import tkinter.messagebox as  mb
import tkinter.ttk as ttk
import requests
import json

from constants import *
from scrollable_frame import *

class MacrotrendsMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #build widgets
        #build title
        row = tk.Frame(self)
        lab = tk.Label(row, text='Macrotrends Menu', font=title_font)
        row.pack(padx=20,pady=15)
        lab.pack()

        #update data button
        #scrapes the website and saves the data in the mongodb database
        row = tk.Frame(self)
        but = tk.Button(row, text='Update Data', width=20,font=font,command=lambda: self.updateData(master))
        row.pack(pady=20)
        but.pack()

        #plot from data graph
        #will take user to a frame that asks for the user to select the fields they would like plotted starting with the categories of the tables
        row = tk.Frame(self)
        but = tk.Button(row, text='Plot Data', width=20, font=font, command=lambda: master.switch_frame(PlotTrendsDataFrame))
        row.pack(pady=20)
        but.pack()

        #back button
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20, command=lambda: self.goBack(master))
        row.pack(pady=10)
        but.pack()

    #function to handle back button clicked
    def goBack(self, master):
        from choose_data_source_frame import ChooseDataSourceFrame
        master.switch_frame(ChooseDataSourceFrame)
    
    #functionto handle updating of the macrotrends database server
    def updateData(self, master):
        #use the macrotrends api to handle data retrieval from website
        from macrotrends_data import MacroTrendsAPI
        api = MacroTrendsAPI(master)

        #TODO:implement api function to get data then send it to the database


#class to handle data selection for plotting of graphs
class PlotTrendsDataFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #listbox counter
        self.counter = 0
        
        #retrieve scrollable frame
        self.frame = ScrollableFrame(master)

        #title
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='Select Plot Options', font=title_font)
        row.pack(pady=15)
        lab.pack()
        
        #define back button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row, text='Back', width=20, command=lambda:self.goBack(master))
        row.pack()
        but.pack()

        #definition of overview options
        self.opts = ['Overview', 'Descriptive', 'Dividends', 'Performance Short Term', 'Performance Long Term', 'Income Ratios', 'Debt Ratios', 'Revenue Earnings']

        for i,opt in enumerate(self.opts):
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text=opt, font=font,width=30,command=lambda i=i: self.optionClick(i))
            row.pack(pady=5)
            but.pack()
    
        self.frame.pack()

    #function to handle clicking on an option
    def optionClick(self, index):
        #get clicked item name
        self.option = self.opts[index]

        #get the columns for this option from database server
        data = {'name' : self.option}
        print('Data : ', json.dumps(data))

        result = requests.post('http://localhost:8080/macrotrends/columns/get',data=json.dumps(data), headers=headers).json()

        if result['success']:
            #build buttons to show the columns 
            self.col_buts = result['headers']

            row = tk.Frame(self.frame.scrollable_frame)
            lab = tk.Label(row, text='Select Column to Plot')
            row.pack(pady=20)
            lab.pack()

            for i,col in enumerate(self.col_buts):
                row = tk.Frame(self.frame.scrollable_frame)
                but = tk.Button(row, text=col,font=font,command=lambda i=i:self.columnClick(i))
                row.pack(pady=5)
                but.pack()
        else:
            mb.showinfo('Notice', result['message'])

    
    #function to handle clicking on an column item
    def columnClick(self, index):
        self.column = self.col_buts[index]
        self.stock_var = tk.StringVary()

        #get the stock information for selection
        result = requests.get(f'{server}/macrotrends/overview/get/all',headers=headers).json()
        print("Result: \n", result)

        #put the stock names in a combobox
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='Select Stocks',font=font)
        self.stocks = ttk.Combobox(row, width=27, textvariable=self.stock_var)
        self.populateStocksCombobox(result)
        row.pack(pady=20)
        lab.pack(side='left')
        self.stocks.pack(side='right')
        self.stocks.current(0)
        self.stocks.bind("<<ComboboxSelected>>", self.stockSelected)

        #have a listbox to display the selected stocks
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        sbar = tk.Scrollbar(row)
        self.listbox = tk.Listbox(row, width=60, height=20)
        sbar.config(command=self.listbox.yview)
        row.pack(pady=5)
        self.listbox.config(yscrollcommand=sbar.set)
        sbar.pack(side='right', fill='y')
        self.listbox.pack(side='left',expand='yes',fill='x', pady=15)
        self.listbox.config(selectmode='single', selectbackground='grey')
        self.listbox.bind("<Double-1>", self.deleteFromListbox)

        #hint about deleting an item
        row = tk.Frame(big_row)
        hint = tk.Label(row, text='hint: double click on list item to remove from list')
        row.pack(pady=15)
        hint.pack()
        big_row.pack()

        #create the plot button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row, text='Plot Button', width=20, font=font, command=lambda: self.plotData(master))
        row.pack()
        but.pack()

    #handles going back
    def goBack(self, master):
        self.frame.destroyMe()
        master.switch_frame(MacrotrendsMenu)

    #handles populating combobox
    def populateStocksCombobox(self, data):
        temp = []

        #for each stock dict get the stock name and append
        for i,stock_dict in enumerate(data):
            temp.append(stock_dict['stock_name'])
        
        self.stocks['values'] = temp

    #handles the selection of a stock and adds it to the listbox
    def stockSelected(self,event):
        selected = event.widget.get()
        self.listbox.insert(self.counter, selected)
        self.counter = self.counter + 1

    #handles deletion from listbox
    def deleteFromListbox(self,event):
        idx = self.listbox.curselection()[0]
        self.listbox.delete(idx)

    #handles plotting of data
    