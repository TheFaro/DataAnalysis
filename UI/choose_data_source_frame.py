import tkinter as tk

import macrotrends_data


class ChooseDataSourceFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # class variables
        self.data_sources = []

        # add IMF as a data source
        self.data_sources.append('International Monetary Fund (IMF) Database')

        # add macrotrends as a data source
        self.data_sources.append('Macro Trends Database')

        # add investing.com as a data source
        self.data_sources.append('Investing.com')

        # build Button to select and facilitate data source
        for i in range(0, len(self.data_sources)):
            Button = tk.Button(
                self, text=self.data_sources[i], width=50, command=lambda i=i: self.buttonClick(master, i))
            Button.pack(pady=10)

        # definition of back button
        tk.Button(self, text='Back', command=lambda: self.goBack(
            master), fg='white', bg='black').pack()

    def goBack(self, master):
        import menu_frame
        master.switch_frame(menu_frame.MenuFrame)

    # handle button click on data source
    def buttonClick(self, master, index):
        import imf_dataset_frame
        import investing_select_data

        if index != None:
            if index == 0:
                # go to next frame
                # frame lists DataFlows or DataSets found in IMF Database/Data source
                master.switch_frame(imf_dataset_frame.IMFDataSetFrame)

            elif index == 1:
                # go to next frame
                # frame
                api = macrotrends_data.MacroTrendsAPI(master)
                selection = 'columns_overview'
                api.getTable(selection)
                # master.switch_frame(MacrotrendsMenu)

            elif index == 2:
                # choose investing.com as a datasource
                master.switch_frame(investing_select_data.SelectData)
