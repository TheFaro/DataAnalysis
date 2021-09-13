import tkinter as tk
import tkinter.messagebox as mb

class SelectData(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self, master)

        self.buildWidgets(master)

    #function to build class widgets
    def buildWidgets(self,master):
        #add values to list
        self.data_list = [
            'Currency Crosses (Forex)',
            'Funds',
            'ETFs',
            'Indices',
            'Stocks',
            'Bonds',
            'Commodities',
            'Cryptocurrency'
        ]

        #build buttons for the data list items
        for (key,value) in enumerate(self.data_list):
            tk.Button(self, text=value, width=40, command=lambda key=key: self.buttonClic(master,key)).pack(pady=10)

        #back button
        tk.Button(self, text='Back', width=20, command=lambda:self.goBack(master)).pack(pady=20)

    #handle back click
    def goBack(self,master):
        from choose_data_source_frame import ChooseDataSourceFrame
        master.switch_frame(ChooseDataSourceFrame)

    #handle item click
    def buttonClic(self, master, index):
        from investing_stocks_frame import PlotDataFrame
        from investing_funds_frame import PlotFundsFrame
        from investing_etfs_frame import PlotEtfsFrame
        from investing_indices_frame import PlotIndicesFrame
        from investing_currency_cross_frame import PlotCrossesFrame
        from investing_bonds_frame import PlotBondsFrame
        from investing_commodities_frame import PlotCommoditiesFrame
        from investing_crypto_frame import PlotCryptosFrame

        if index == 0:
            master.switch_frame(PlotCrossesFrame)

        if index == 1:
            master.switch_frame(PlotFundsFrame)

        if index == 2: 
            master.switch_frame(PlotEtfsFrame)

        if index == 3:
            master.switch_frame(PlotIndicesFrame)

        if index == 4:
            master.switch_frame(PlotDataFrame)
        
        if index == 5:
            master.switch_frame(PlotBondsFrame)

        if index == 6:
            master.switch_frame(PlotCommoditiesFrame)

        if index == 7:
            master.switch_frame(PlotCryptosFrame)