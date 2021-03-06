import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import investpy
import pandas as pd
import datetime
import json
import requests

import investing_bonds_api
import constants as const


class PlotBondsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.country_var = tk.StringVar()
        self.bond_var = tk.StringVar()
        self.api = investing_bonds_api.BondsAPI()
        self.const = const.Constants()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Bonds Plotting', font=self.const.title_font)
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

        # combobox for selecting bond
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Bond', font=self.const.font)
        self.bonds = ttk.Combobox(row, width=27, textvariable=self.bond_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.bonds.pack(side='right')
        self.bonds.bind("<<ComboboxSelected>>", self.bondSelected)

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
        big_row = tk.Frame(self)
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

    # function to populate countries combobox
    def populateCountriesCombobox(self, master):
        countries = self.api.getCountries()
        temp = []

        # append each item to the combobox values
        for i, country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp

    # function to handle selection of country
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        # get bonds dict for bonds combobox
        bonds = investpy.get_bonds_dict(country=selected, as_json=True)
        bonds_list = json.loads(bonds)
        print('Bonds List: \n', bonds_list)
        temp = []

        # for each bond append into combobox values
        for i, bond in enumerate(bonds_list):
            #print('Index: ', i, '\n', bond)
            temp.append(bond["name"])

        self.bonds['values'] = temp
        print(self.bonds['value'])

    # function to handle the selection bond
    def bondSelected(self, event):
        selected = event.widget.get()
        self.api.setBond(selected)

    # function to handle plotting of graphs
    def plotData(self, master):
        # check for inputs
        if self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a country')
            return
        elif self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a bond')
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

        historical = self.api.getBondData()
        j = json.loads(historical)
        data = j['historical']

        df = pd.DataFrame(data)
        self.const.drawCandles(df, self.api.getName(), self.api.getCountry)

    # function to handle updating data in database server

    def updateData(self):
        # check for bond
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a bond')
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a country')

        # get most recent
        data = {
            'bond_name': f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f'{self.const.server}/investing/bonds/get/recent',
                              data=json.dumps(data), headers=self.const.headers)

        if recent.status_code == 404:
            # get historical data
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getBondData()
            j = json.loads(historical)
            dat = j['historical']

            # send data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/bonds', 'bond_name', self.api)

            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')
        elif recent.status_code == 200:
            # get recent data
            rec = recent.json()
            print('\n', rec, '\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']

            print('Recent Date', recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getBondData()
            j = json.loads(historical)
            dat = j['historical']

            # save data to mongodb server
            self.const.saveDataInServer(
                dat, 'investing/bonds', 'bond_name', self.api)
            mb.showinfo(
                'Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent['message'])
