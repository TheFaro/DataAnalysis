import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

from investing_bonds_api import *
from scrollable_frame import *
import constants as const

class PlotBondsFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.country_var = tk.StringVar()
        self.bond_var = tk.StringVar()
        self.api = BondsAPI()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Bonds Plotting',font=const.title_font)
        row.pack()
        lab.pack()

        #combobox for selecting country
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Country', font=const.font)
        self.countries = ttk.Combobox(row, width=27, textvariable=self.country_var)
        self.populateCountriesCombobox(master)
        row.pack(pady=15)
        lab.pack(side='left')
        self.countries.pack(side='right')
        self.countries.current(0)
        self.countries.bind("<<ComboboxSelected>>", self.countrySelected)

        #combobox for selecting bond
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Bond', font=const.font)
        self.bonds = ttk.Combobox(row, width=27, textvariable=self.bond_var)
        row.pack(pady=15)
        lab.pack(side='left')
        self.bonds.pack(side='right')
        self.bonds.bind("<<ComboboxSelected>>", self.bondSelected)

        #start date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='Start Date', width=30, font=const.font, relief='ridge')
        self.start_date = tk.Entry(row, width=25, font=const.font,relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.start_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd/mm/yyyy)',font=const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        #end date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='End Date', width=30, font=const.font, relief='ridge')
        self.end_date = tk.Entry(row, width=25, font=const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.end_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd/mm/yyyy)',font=const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        #plot button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Plot Data', font=const.font, width=20, command=lambda:self.plotData(master))
        row.pack(pady=15)
        but.pack()

        #update all definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Update All', font=const.font,width=20)
        row.pack(pady=15)
        but.pack()

        #back button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20, command=lambda: self.goBack(master))
        row.pack(pady=15)
        but.pack()

    #handle back button click
    def goBack(self, master):
        from investing_select_data import SelectData
        master.switch_frame(SelectData)

    #function to populate countries combobox
    def populateCountriesCombobox(self,master):
        countries = self.api.getCountries()
        temp = []

        #append each item to the combobox values
        for i,country in enumerate(countries):
            temp.append(country)

        self.countries['values'] = temp
    
    #function to handle selection of country 
    def countrySelected(self, event):
        selected = event.widget.get()
        self.api.setCountry(selected)

        #get bonds dict for bonds combobox
        bonds = self.api.getBondsDict(country=selected)
        temp = []

        #for each bond append into combobox values
        for i,bond in enumerate(bonds):
            temp.append(bond['name'])

        self.bond['values'] = temp

    #function to handle the selection bond 
    def bondSelected(self,event):
        selected = event.widget.get()
        self.api.setBond(selected)

    #function to handle plotting of graphs
    def plotData(self, master):
        #check for inputs
        if self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a country')
            return
        elif self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a bond')
            return
        '''elif self.start_date.get() == None or self.start_date.get() == "":
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None or self.end_date.get() == "":
            mb.showinfo('Notice', 'Enter end date')
            return'''
        
        #check for date in mongo db server
        result = requests.get(f"{const.server}/investing/bonds/get/{self.api.getName()}_{self.api.getCountry()}/{self.start_date.get().replace('/','')}/{self.end_date.get().replace('/','')}", headers=const.headers).json()
        print('Result for getting:',result['data'][0]['data'])
        
        if result['success'] == 1:
            df = pd.DateFrame(result['data'][0]['data'])
            print('DataFrame: \n',df)
            
            #drop unwanted column // __id
            df.drop(df.columns[[0]], axis=1, inplace=True)

            #draw candles
            const.drawCandles(df,self.api.getName(), self.api.getCountry())
        else: 
            self.updateData()
            self.plotData(master)

    #function to handle updating data in database server
    def updateData(self):
        #check for bond 
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', 'Select a bond')
            return
        elif self.api.getCountry() == None or self.api.getCountry() == "":
            mb.showinfo('Notice', 'Select a country')

        #get most recent 
        data = {
            'bond_name' : f"{self.api.getName()}_{self.api.getCountry()}"
        }

        recent = requests.get(f'{const.server}/investing/bonds/get/recent',data=json.dumps(data),headers=const.headers)
        
        if recent.status_code == 404: 
            #get historical data
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getBondData()
            j = json.loads(historical)
            dat = j['historical']

            #send data to mongodb server
            const.saveDataInServer(dat,'investing/bonds','bond_name',self.api)
            
            mb.showinfo('Notice', f'Data on {self.api.getName()} updated successfully.')
        elif recent.status_code == 200:
            #get recent data
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

            #save data to mongodb server
            const.saveDataInServer(dat, 'investing/bonds', 'bond_name', self.api)
            mb.showinfo('Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', r['message'])