import tkinter as tk

import choose_data_source_frame
import imf_series_dataflow_frame


class IMFDataSetFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.sets_list = []
        self.master = master

        # add data sets to the list
        '''self.sets_list.append({"code": "FSI","name": "Financial Soundness Indicators"})
        self.sets_list.append({"code": "FAS","name": "Financial Access Survey"})
        self.sets_list.append({"code": "IFS","name": "International Financial Statistics"})
        self.sets_list.append({"code": "MCDREP","name": "Middle East and Central Asia Regional Economic Outlook"})
        self.sets_list.append({"code": "DOTS","name": "Direction of Trade Statistics"})
        self.sets_list.append({"code": "CDIS","name": "Coordinated Direct Investment Survey"})
        self.sets_list.append({"code": "GFS","name": "Government Finance Statistics"})
        self.sets_list.append({"code": "BOP","name": "Balance Of Payments"})
        self.sets_list.append({"code": "CPIS","name": "Coordinated Portfolio Investment Survey"})
        self.sets_list.append({"code": "APDREO","name": "Asia and Pacific Regional Economic Outlook"})
        self.sets_list.append({"code": "FM","name": "Fiscal Monitor"})
        self.sets_list.append({"code": "AFRREO","name": "Sub-Saharan Africa Regional Economic Outlook"})
        self.sets_list.append({"name": "Primary Commodity Prices"})
        self.sets_list.append({"code": "WoRLD","name": "World Revenue Longitudinal Data"})
        self.sets_list.append({"code": "PGI","name": "Principal Global Indicators"})
        self.sets_list.append({"code": "WHDREO","name": "Western Hemisphere Regional Economic Outlook"})
        self.sets_list.append({"code": "WCED","name": "World Commodity Exports"})
        self.sets_list.append({"code": "ICSD","name": "Investment and Capital Stock"})
        self.sets_list.append({"code": "HPDD","name": "Historical Public Debt"})
        self.sets_list.append({"code": "COFR","name": "Coverage of Fiscal Reporting"})
        self.sets_list.append({"code": "CPI","name": "Consumer Price Index"})
        self.sets_list.append({"code": "IRFCL","name": "International Reserves and Foriegn Currency Liquidity"})
        self.sets_list.append({"code": "COFER","name": "Currency Composition Of Official Foreign Exchange Reserves"})
        self.sets_list.append({"code": "MFS","name": "Monetary and Financial Statistics"})
        self.sets_list.append({"code": "SNA","name": "System of National Accounts"})'''

        # create widgets
        self.search_text = tk.StringVar()
        self.search_text.set("IMF - DataSets")
        tk.Label(self, textvariable=self.search_text,
                 width="40").pack(side=tk.TOP)

        # search bar
        edit = tk.Entry(self)
        edit.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        edit.focus_set()

        # add search button
        tk.Button(self, text='Search', command=lambda: self.setSearchTerm(
            edit.get())).pack(side=tk.TOP, pady=15)

        # add get all button
        tk.Button(self, text='Get All Data Sets',
                  command=lambda: self.getAll()).pack(side=tk.TOP, pady=10)

        # define a back button
        back_button = tk.Button(self, text="Back", command=lambda: self.master.switch_frame(
            choose_data_source_frame.ChooseDataSourceFrame))
        back_button.pack(side=tk.BOTTOM, pady=15)

        # create a list box with current dataset list
        '''scrollbar = tk.Scrollbar(self)
        list = tk.Listbox(self,relief=SUNKEN,width="60",height="20")
        scrollbar.config(command=list.yview)
        list.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT,fill=Y)
        list.pack(side=tk.LEFT, expand=YES, fill=X,pady=15)

        for i in range(len(self.sets_list)):
            list.insert(i, self.sets_list[i]["name"])
            
        list.config(selectmode=SINGLE,setgrid=1)
        list.bind('<Double-1>', self.selectedDataset)
        self.list_box = list'''

    # function that retrieves selected dataset code
    def selectedDataset(self, event):
        index = self.list_box.curselection()
        idx = index[0]

        # set selected dataset code
        self.master.setIMFDatasetCode(self.sets_list[idx]['code'])

    # function to set search term
    def setSearchTerm(self, term):
        self.master.setIMFSearchString(term)
        self.master.switch_frame(
            imf_series_dataflow_frame.SearchForSeriesDataflow)

    # function to get all datasets
    def getAll(self):
        self.master.search_term = ""
        self.master.switch_frame(
            imf_series_dataflow_frame.SearchForSeriesDataflow)
