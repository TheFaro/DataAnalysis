import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

import investing_crypto_api
import constants as const


class PlotCryptosFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.crypto_var = tk.StringVar()
        self.api = investing_crypto_api.CryptoAPI()
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Cryptos Plotting',
                       font=self.const.title_font)
        row.pack()
        lab.pack()

        # combobox for selecting crypto
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Crypto', font=self.const.font)
        self.cryptos = ttk.Combobox(
            row, width=27, textvariable=self.crypto_var)
        self.populateCryptosCombobox(master)
        row.pack(pady=15)
        lab.pack(side='left')
        self.cryptos.pack(side='right')
        self.cryptos.current(0)
        self.cryptos.bind("<<ComboboxSelected>>", self.cryptoSelected)

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
        but = tk.Button(row, text='Update', font=self.const.font,
                        width=20, command=lambda: self.updateData())
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

    # function to populate combobox
    def populateCryptosCombobox(self, master):
        cryptos = self.api.getCryptoDict()
        temp = []

        # append each item to combobox
        for i, crypto in enumerate(cryptos):
            temp.append(crypto['name'])

        self.cryptos['values'] = temp

    # handle combobox selected
    def cryptoSelected(self, event):
        selected = event.widget.get()
        self.api.setCrypto(selected)

    # handle plotting graphs
    def plotData(self, master):
        # check for inputs
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a crypto')
            return
        elif self.start_date.get() == None or self.start_date.get() == "":
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None or self.end_date.get() == "":
            mb.showinfo('Notice', 'Enter end date')
            return

        # get data from investing database
        self.api.setFromDate(self.start_date.get())
        self.api.setToDate(self.end_date.get())

        # get historical data
        historical = self.api.getCryptoData()
        j = json.loads(historical)
        data = j['historical']

        # create dataframe
        df = pd.DataFrame(data)
        self.const.drawCandles(df, self.api.getName(), '')

    # function to handle updating data in database server

    def updateData(self):
        # check for crypto
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a crypto')
            return

        # get most recent
        data = {
            'crypto_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f'{self.const.server}/investing/crypto/get/recent',
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getCryptoData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/crypto', 'crypto_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')
        elif recent.status_code == 200:
            # get recent data
            rec = recent.json()
            #recent_date = rec['date']
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print("Recent Date", recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getCryptoData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/crypto', 'crypto_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])
