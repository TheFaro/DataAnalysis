import tkinter as tk

from menu_frame import *
from macrotrends_data import *

class ChooseDataSourceFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)

        #class variables
        self.data_sources = []

        #add IMF as a data source
        self.data_sources.append('International Monetary Fund (IMF) Database')
        
        #add macrotrends as a data source
        self.data_sources.append('Macro Trends Database')

        #add investing.com as a data source
        self.data_sources.append('Investing.com')

        #build Button to select and facilitate data source
        for i in range(0, len(self.data_sources)):
            Button = tk.Button(self,text=self.data_sources[i],width=50,command=lambda i=i: self.buttonClick(master,i))
            Button.pack(pady=10)

        #definition of back button
        tk.Button(self,text='Back',command=lambda:self.goBack(master),fg='white',bg='black').pack()

    def goBack(self, master):
        from menu_frame import MenuFrame
        master.switch_frame(MenuFrame)

    #handle button click on data source
    def buttonClick(self, master, index):
        from imf_dataset_frame import IMFDataSetFrame
        from investing_select_data import SelectData
        from macrotrends_menu import MacrotrendsMenu

        if index != None:
            if index == 0: 
                #go to next frame
                #frame lists DataFlows or DataSets found in IMF Database/Data source
                master.switch_frame(IMFDataSetFrame)
            
            elif index == 1: 
                #go to next frame
                #frame
                api = MacroTrendsAPI(master)
                selection = 'columns_overview'
                api.getTable(selection)
                #master.switch_frame(MacrotrendsMenu)

            elif index == 2:
                #choose investing.com as a datasource
                master.switch_frame(SelectData)
