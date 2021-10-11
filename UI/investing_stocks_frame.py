import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from time import sleep
import pandas as pd
import datetime
import json
import requests

import investing_stocks_api
import constants as const

# class to handle getting and displaying company profile


class PlotDataFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.stock_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.api = investing_stocks_api.StocksAPI(master)
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Stock Plotting', font=self.const.title_font)
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

        # combobox to select stock
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Stock Name', font=self.const.font)
        self.stocks = ttk.Combobox(row, width=27, textvariable=self.stock_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.stocks.pack(side='right')
        self.stocks.bind("<<ComboboxSelected>>", self.stockSelected)

        # definition of Text widget to display stock information after retrieval
        '''row = tk.Frame(self)
        self.display = tk.Text(row, bg='white', wrap=tk.WORD, font=self.const.font, width=60, height=10)
        row.pack(pady=15)
        self.display.pack()'''

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

        # back button
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20,
                        command=lambda: self.goBack(master))
        row.pack(pady=10)
        but.pack()

    # handles back button click
    def goBack(self, master):
        import investing_select_data
        master.switch_frame(investing_select_data.SelectData)

    # function to populate the countries
    def populateCountriesCombobox(self, master):
        countries = self.api.getStockCountries()
        temp = []

        # for each item in the list append into combobox
        for i, country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp

    # function to handle selection of country in combobox as well as retrieving appropriate stocks for that country
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        print('Country:')
        print(selected)

        # delete any data showing
        '''if len(self.display.get('1.0','end-1c')) != 0:
            self.display.delete('1.0',tk.END)
            self.api.setCountry(None)
            self.api.setStock(None)'''

        # get the stocks for the stocks combo box
        stocks = self.api.getStocksDict(country=selected)
        temp = []

        # for each item append to stocks comboxbox
        for i, stock in enumerate(stocks):
            temp.append(stock['full_name'])

        self.stocks['values'] = temp

    # function to handle selecting stock
    def stockSelected(self, event):
        selected = event.widget.get()
        self.api.setStock(selected)
        print("Stock")
        print(selected)

    # function to handle plotting of data from selected parameters.
    def plotData(self, master):
        if self.api.getName() == None or self.api.getName() == '':
            mb.showinfo('Notice', 'Select a Stock')
            return
        elif self.api.getCountry() == None or self.api.getName() == '':
            mb.showinfo('Notice', 'Select a Country')
            return

        # check start date and end date
        if self.start_date.get() == None:
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None:
            mb.showinfo('Notice', 'Enter end date')
            return

        # get data from investing database
        self.api.setFromDate(self.start_date.get())
        self.api.setToDate(self.end_date.get())

        # get historical data
        historical = self.api.getStockData()

        print('Stock: ', self.api.getName())
        print('Country: ', self.api.getCountry())
        print('Start Date: ', self.api.getFromDate())
        print('End Date: ', self.api.getToDate())

        # parse json
        j = json.loads(historical)
        data = j['historical']

        # create dataframe
        df = pd.DataFrame(data)
        self.const.drawCandles(df, self.api.getName(), self.api.getCountry())

    # function to handle updating data in the database server
    def updateData(self):
        # input stock name and country name
        if self.api.getName() == None or self.api.getName() == '':
            mb.showinfo('Notice', 'Select a Stock')
            return
        elif self.api.getCountry() == None or self.api.getCountry() == '':
            mb.showinfo('Notice', 'Select a Country')
            return

        data = {
            'stock_name': f"{self.api.getStock()}_{self.api.getCountry()}"
        }

        # get most recent record from server
        recent = requests.get(f"{self.const.server}/investing/stocks/get/recent",
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data from 01/01/1980 to Date.now - 1 day
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime("%d/%m/%Y"))

            historical = self.api.getStockData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/stocks', 'stock_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully')

        elif recent.status_code == 200:
            # get recent data for the country and stock
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print('Recent Date', recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getStockData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/stocks', 'stock_name', self.api)

            mb.showinfo(
                'Notice', f"Data on {self.api.getName()} updated successfully.")

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])
        # continue exection of program after updating.
