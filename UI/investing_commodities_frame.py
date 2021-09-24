import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

import investing_commodities_api
import constants as const


class PlotCommoditiesFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.group_var = tk.StringVar()
        self.commodity_var = tk.StringVar()
        self.api = investing_commodities_api.CommoditiesAPI()
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Commodities Plotting',
                       font=self.const.title_font)
        row.pack()
        lab.pack()

        # combobox for selecting group
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Group', font=self.const.font)
        self.groups = ttk.Combobox(row, width=27, textvariable=self.group_var)
        self.populateGroupsCombobox(master)
        row.pack(pady=15)
        lab.pack(side='left')
        self.groups.pack(side='right')
        self.groups.current(0)
        self.groups.bind("<<ComboboxSelected>>", self.groupSelected)

        # combobox for selecting commodity
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Commodity', font=self.const.font)
        self.commodities = ttk.Combobox(
            row, width=27, textvariable=self.commodity_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.commodities.pack(side='right')
        self.commodities.bind("<<ComboboxSelected>>", self.commoditySelected)

        # start date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='Start Date', width=30,
                       font=self.const.font, relief='ridge')
        self.start_date = tk.Entry(
            row, width=25, font=self.const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.start_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd/mm/yyyy)',
                        font=self.const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        # end date definition
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='End Date', width=30,
                       font=self.const.font, relief='ridge')
        self.end_date = tk.Entry(
            row, width=25, font=self.const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.end_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd/mm/yyyy)',
                        font=self.const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        # plot button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Plot Data', font=self.const.font,
                        width=20, command=lambda: self.plotData(master))
        row.pack(pady=15)
        but.pack()

        # update all definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Update All', font=self.const.font, width=20)
        row.pack(pady=15)
        but.pack()

        # back button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20,
                        command=lambda: self.goBack(master))
        row.pack(pady=15)
        but.pack()

    # handle back button click
    def goBack(self, master):
        import investing_select_data
        master.switch_frame(investing_select_data.SelectData)

    # function to populate the groups combobox
    def populateGroupsCombobox(self, master):
        groups = self.api.getGroups()
        temp = []

        # append each item to groups combobox
        for i, group in enumerate(groups):
            temp.append(group)

        self.groups['values'] = temp

    # handle group selection
    def groupSelected(self, event):
        selected = event.widget.get()
        self.api.setGroup(selected)

        # retrieve commodities based on selected group
        commodities = self.api.getCommoditiesDict(group=selected)
        temp = []

        # append each item to the commodities combobox
        for i, commodity in enumerate(commodities):
            temp.append(commodity['name'])

        self.commodities['values'] = temp

    # handle the selection of a commodity
    def commoditySelected(self, event):
        selected = event.widget.get()
        self.api.setCommodity(selected)

    # handle plotting of graphs using specified data
    def plotData(self, master):
        # check for inputs
        if self.api.getGroup() == None or self.api.getGroup() == "":
            mb.showinfo('Notice', 'Select a group')
            return
        elif self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a commodity')
            return
        '''elif self.start_date.get() == None or self.start_date.get() == "":
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None or self.end_date.get() == "":
            mb.showinfo('Notice', 'Enter end date')
            return
        '''

        # check for date in mongo db server
        result = requests.get(
            f"{self.const.server}/investing/commodities/get/{self.api.getName()}_{self.api.getCountry()}/{self.start_date.get().replace('/','')}/{self.end_date.get().replace('/','')}", headers=self.const.headers).json()

        if result['success'] == 1:
            df = pd.DateFrame(result['data'][0]['data'])
            print('DataFrame: \n', df)

            # drop unwanted columns // __id, volume, currency
            df.drop(df.columns[[0, 6, 7]], axis=1, inplace=True)

            # draw candles
            self.const.drawCandles(
                df, self.api.getName(), self.api.getCountry())
        else:
            self.updateData()
            self.plotData(master)

    # function to handle updating data in database server
    def updateData(self):
        # check for bond
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a commodity')
            return
        elif self.api.getGroup() == None or self.api.getGroup() == "":
            mb.showinfo('Notice', 'Select a group')

        # get most recent
        data = {
            'commodity_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f'{self.const.server}/investing/commodities/get/recent',
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getCommodityData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/commodities', 'commodity_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 200:
            # get recent data
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']

            print('Recent Date:', recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.setToDate(now.strftime('%d-%m-%Y'))

            historical = self.api.getCommodityData()
            j = json.loads(historical)
            dat = j['historical']

            # save data to mondo db server
            self.const.saveDataInServer(
                dat, 'investing/commodities', 'commodity_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent['message'])
