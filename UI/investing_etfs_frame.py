import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

import investing_etfs_api
import constants as const


class PlotEtfsFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self,  master)

        self.etf_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.api = investing_etfs_api.ETFSAPI()
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='ETF Plotting', font=self.const.title_font)
        row.pack()
        lab.pack()

        # combobox for selecting country
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Country', font=self.const.font)
        self.countries = ttk.Combobox(
            row, width=27, textvariable=self.country_var)
        self.populateCountriesCombobox(master)
        row.pack(pady=15)
        lab.pack(side='left')
        self.countries.pack(side='right')
        self.countries.current(0)
        self.countries.bind("<<ComboboxSelected>>", self.countrySelected)

        # combobox for selecting etfs
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select etf name', font=self.const.font)
        self.etfs = ttk.Combobox(row, width=27, textvariable=self.etf_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.etfs.pack(side='right')
        self.etfs.bind("<<ComboboxSelected>>", self.etfSelected)

        # start date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='Start Date',
                       font=self.const.font, width=30, relief='ridge')
        self.start_date = tk.Entry(
            row, width=25, font=self.const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.start_date.pack(side='right')

        row = tk.Frame(self)
        hint = tk.Label(row, text='date format (dd/mm/yyyy)',
                        font=self.const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        # end date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='End Date',
                       font=self.const.font, width=30, relief='ridge')
        self.end_date = tk.Entry(
            row, width=25, font=self.const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.end_date.pack(side='right')

        row = tk.Frame(self)
        hint = tk.Label(row, text='date format (dd/mm/yyyy',
                        font=self.const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        # plot button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Plot Data', width=20,
                        font=self.const.font, command=lambda: self.plotData(master))
        row.pack(pady=15)
        but.pack()

        # update all button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Update All', width=20, font=self.const.font)
        row.pack(pady=15)
        but.pack()

        # back button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20,
                        command=lambda: self.goBack(master))
        row.pack(pady=10)
        but.pack()

    # handles going back
    def goBack(self, master):
        import investing_select_data
        master.switch_frame(investing_select_data.SelectData)

    # function to populate countries
    def populateCountriesCombobox(self, master):
        countries = self.api.getEtfsCountries()
        temp = []

        # for each item append into combobox
        for i, country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp

    # function to handle when a country is selected in combobox and retrieve appropriate etf values
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        # get etfs for etfs combobox
        etfs = self.api.getEtfsDict(country=selected)
        temp = []

        for i, etf in enumerate(etfs):
            temp.append(etf['name'])

        self.etfs['values'] = temp

    # function to handle selection of a fund
    def etfSelected(self, event):
        selected = event.widget.get()
        self.api.setEtfs(selected)

    # function to handle plotting of data from selected parameters
    def plotData(self, master):
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', "Select ETF value")
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', "Select Country")
            return

        # check start date and end date
        if self.start_date.get() == None or self.start_date.get() == "":
            mb.showinfo('Notice', "Specify start date")
            return
        elif self.end_date.get() == None or self.end_date.get() == "":
            mb.showinfo('Notice', "Specify end date")
            return

        # retrieve data from investing database
        self.api.setFromDate(self.start_date.get())
        self.api.setToDate(self.end_date.get())

        # get historical data
        historical = self.api.getEtfData()
        print(historical)

        # parse json
        j = json.loads(historical)
        data = j['historical']

        # create dataframe from dataset
        df = pd.DataFrame(data)
        print('DataFrame: \n', df)

        # draw candles
        self.const.drawCandles(df, self.api.getName(), self.api.getCountry())

    # function to update data in database server

    def updateData(self):
        # check etf and country name
        if self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', "Select a Country")
            return
        elif self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', "Select etf")
            return

        # get most recent record from server with this name
        data = {
            'etfs_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f"{self.const.server}/investing/etfs/get/recent",
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data starting from 1980
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getEtfData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/etfs', 'etfs_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 200:
            # get recent data for the country and etf
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print("Recent Date", recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getEtfData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/etfs', 'etfs_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])
