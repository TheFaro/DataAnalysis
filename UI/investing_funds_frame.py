import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import requests
import json

import investing_funds_api
import constants as const


class PlotFundsFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fund_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.api = investing_funds_api.FundsAPI(master)
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Funds Plotting', font=self.const.title_font)
        row.pack()
        lab.pack()

        # combobox to select country
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

        # combobox to select fund
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Fund Name', font=self.const.font)
        self.funds = ttk.Combobox(row, width=27, textvariable=self.fund_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.funds.pack(side='right')
        self.funds.bind("<<ComboboxSelected>>", self.fundsSelected)

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

        row = tk.Frame(big_row)
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

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format (dd/mm/yyyy)',
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
        countries = self.api.getFundsCountries()
        temp = []

        # for each item append into combobox
        for i, country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp

    # function to handle selection of country in combobox and retrieve appropriate funds
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        # get funds for funds combobox
        funds = self.api.getFundsDict(country=selected)
        temp = []

        # for each item append into funds combobox
        for i, fund in enumerate(funds):
            temp.append(fund['name'])

        self.funds['values'] = temp

    # function to handle selecting fund
    def fundsSelected(self, event):
        print('Country:')
        print(self.api.getCountry())
        print('I am heres')
        selected = event.widget.get()
        self.api.setFund(selected)
        print('Fund:')
        print(self.api.getName())

    # function to handle plotting of data from selected parameters.
    def plotData(self, master):
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a Fund')
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a Country')
            return

        # check start date and end date
        '''if self.start_date.get() == None:
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None:
            mb.showinfo('Notice', 'Enter end date')  
            return'''

        # first check for data in database
        result = requests.get(
            f"{self.const.server}/investing/funds/get/{self.api.getName()}_{self.api.getCountry()}/{self.start_date.get().replace('/','')}/{self.end_date.get().replace('/','')}", headers=self.const.headers).json()
        print('Result for getting:', result['data'][0]['data'])

        if result['success'] == 1:
            df = pd.DataFrame(result['data'][0]['data'])
            print('DataFrame: \n', df)

            # dropping unnecessary columns
            df.drop(df.columns[[0, 6, 7]], axis=1, inplace=True)

            # draw candles
            self.const.drawCandles(
                df, self.api.getName(), self.api.getCountry())
        else:
            # update data
            self.updateData()
            self.plotData(master)

    # function to handle updating data in the database server
    def updateData(self):
        # input fund name and country name
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a Fund')
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a Country')
            return

        # get most recent record from server
        data = {
            'fund_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f"{self.const.server}/investing/funds/get/recent",
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data from 01/01/1980 to Date.now - 1 day
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime("%d/%m/%Y"))

            historical = self.api.getFundData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/funds', 'fund_name', self.api)

            mb.showinfo('Notice', f'Data on {self.api.getFund()} updated.')
        elif recent.status_code == 200:
            # get recent data for the country and stock
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print("Recent Date", recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getFundData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/funds', 'fund_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getFund()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])
        # continue exection of program after updating.
