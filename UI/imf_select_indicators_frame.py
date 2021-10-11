import tkinter as tk
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sb

import imf_select_countries_frame
import imf_data_processor
import choose_data_source_frame


class SelectIndicatorsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        # create listbox to display indicators and handle click on one
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self, width="60", height="20")
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, pady=15)
        self.listbox.config(selectmode=tk.SINGLE, selectbackground='grey')
        self.listbox.bind('<Double-1>', self.getDataFromDataSource)

        for i, indicator in enumerate(self.master.indicator_list):
            self.listbox.insert(i, indicator['text'])

        tk.Button(self, text='Back', command=lambda: master.switch_frame(
            imf_select_countries_frame.SelectCountriesFrame)).pack(side=tk.TOP)
        tk.Button(self, text='Go Back Data Source Select', command=lambda: master.switch_frame(
            choose_data_source_frame.ChooseDataSourceFrame)).pack(side=tk.TOP)

    def getDataFromDataSource(self, event):
        index = self.listbox.curselection()[0]
        print(self.master.indicator_list[index]["code"])
        if len(self.master.IMF_var) < 3:
            self.master.IMF_var.append(
                {'indicator': f'{self.master.indicator_list[index]["code"]}'})
        else:
            self.master.IMF_var[2] = {
                'indicator': f'{self.master.indicator_list[index]["code"]}'}
        print(self.master.IMF_var[2])

        data_processor = imf_data_processor.IMFDataProcessor(self.master)
        data_processor.getData()
        # data_processor.getIMFDataFromServer()
        print(data_processor.total_df)

        if data_processor.total_df == None or data_processor.total_df.empty == False:
            ax = sb.lineplot(data=data_processor.total_df)
            ax.set(xlabel="Date", ylabel="Symbol")
            plt.show()
        else:
            print('No data available for plotting')
