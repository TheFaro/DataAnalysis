import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

import investing_indices_api
import constants as const


class PlotIndicesFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.index_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.api = investing_indices_api.IndicesAPI()
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Indices Plotting',
                       font=self.const.title_font)
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

        # combobox for selecting index
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Index', font=self.const.font)
        self.indices = ttk.Combobox(row, width=27, textvariable=self.index_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.indices.pack(side='right')
        self.indices.bind("<<ComboboxSelected>>", self.indexSelected)

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
        hint = tk.Label(row, text='date format (dd/mm/yyyy)',
                        font=self.const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        # end date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='End Date', font=self.const.font,
                       width=30, relief='ridge')
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
        but = tk.Button(row, text="Plot Data", font=self.const.font,
                        width=20, command=lambda: self.plotData(master))
        row.pack(pady=15)
        but.pack()

        # update all Button
        row = tk.Frame(self)
        but = tk.Button(row, text='Update All', font=self.const.font, width=20)
        row.pack(pady=15)
        but.pack()

        # back button
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20,
                        command=lambda: self.goBack(master))
        row.pack(pady=15)
        but.pack()

    # handle back button
    def goBack(self, master):
        import investing_select_data
        master.switch_frame(investing_select_data.SelectData)

    # function to populate countries combobox
    def populateCountriesCombobox(self, master):
        countries = self.api.getIndicesCountries()
        temp = []

        # append each country to combobox array
        for i, country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp

    # function to handle country selection in combobox
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        # get indices dict for indices combobox
        indices = self.api.getIndicesDict(country=selected)
        temp = []

        # populate the indices combobox
        for i, index in enumerate(indices):
            temp.append(index['name'])

        self.indices['values'] = temp

    # function to handle selection of index in combobox
    def indexSelected(self, event):
        selected = event.widget.get()
        self.api.setIndex(selected)

    # function to handle plotting of data
    def plotData(self, master):
        # check for inputs
        if self.api.getCountry() == None or self.api.getCountry() == '':
            mb.showinfo('Notice', 'Select a Country')
            return
        elif self.api.getName() == None or self.api.getName() == '':
            mb.showinfo('Notice', 'Select an Index')
            return
        '''elif self.start_date.get() == None or self.start_date.get() == '':
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None or self.end_date.get() == '':
            mb.showinfo('Notice', 'Enter end date')
            return
        '''
        # check for data in mongo db server
        result = requests.get(
            f"{self.const.server}/investing/indices/get/{self.api.getName()}_{self.api.getCountry()}/{self.start_date.get().replace('/','')}/{self.end_date.get().replace('/','')}", headers=self.const.headers).json()
        print("Result for getting: ", result['data'][0]['data'])

        if result['success'] == 1:
            df = pd.DataFrame(result['data'][0]['data'])
            print('DataFrame: \n', df)

            df.drop(df.columns[[0, 6, 7]], axis=1, inplace=True)

            # draw candles
            self.const.drawCandles(
                df, self.api.getName(), self.api.getCountry())
        else:
            self.updateData()
            self.plotData(master)

    # function to update data in database server
    def updateData(self):
        # check for index name and country name
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', "Select an Index")
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select Country')
            return

        # get most recent record from server with this name
        data = {
            'index_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f"{self.const.server}/investing/indices/get/recent",
                              data=json.dumps(data), headers=self.const.headers)
        print(recent)

        if recent.status_code == 404:
            # get historical data starting from 1980
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.toDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getIndexData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/indices', 'index_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 200:
            # get recent data
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data'][0]
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print('Recent Date', recent_date)

            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getIndexData()
            j = json.loads(historical)
            data = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                data, 'investing/indices', 'index_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')
        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])
