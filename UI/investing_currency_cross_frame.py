import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
import pandas as pd
import datetime
import json
import requests

from investing_currency_cross_api import *
from scrollable_frame import *
import constants as const

class PlotCrossesFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.cross_var = tk.StringVar()
        self.api = CrossesAPI()

        row = tk.Frame(self)
        lab = tk.Label(row, text='Currency Crosses Plotting', font=const.title_font)
        row.pack()
        lab.pack()

        #combobox for selecting currency crosses
        row = tk.Frame(self)
        lab = tk.Label(row, text='Select Currency Cross', font=const.font)
        self.crosses = ttk.Combobox(row, width=27, textvariable=self.cross_var)
        self.populateCrossesCombobox(master)
        row.pack(pady=15)
        lab.pack(side='left')
        self.crosses.pack(side='right')
        self.crosses.current(0)
        self.crosses.bind("<<ComboboxSelected>>", self.crossSelected)

        #start date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='Start Date',width=30, font=const.font, relief='ridge')
        self.start_date = tk.Entry(row, width=25, font=const.font, relief='sunken')
        row.pack()
        lab.pack(side='left')
        self.start_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format (dd/mm/yyyy)',font=const.hint_font)
        row.pack()
        hint.pack()
        big_row.pack(pady=15, padx=10)

        #end date definition
        big_row = tk.Frame(self)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='End Date', font=const.font, width=30, relief='ridge')
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
        but = tk.Button(row, text="Plot Data", font=const.font, width=20, command=lambda: self.plotData(master))
        row.pack(pady=15)
        but.pack()

        #update all Button
        row = tk.Frame(self)
        but = tk.Button(row, text='Update All', font=const.font, width=20)
        row.pack(pady=15)
        but.pack()

        #back button
        row = tk.Frame(self)
        but = tk.Button(row, text='Back', width=20, command=lambda:self.goBack(master))
        row.pack(pady=15)
        but.pack()

    #handle going back
    def goBack(self, master):
        from investing_select_data import SelectData
        master.switch_frame(SelectData)
    
    #function to populate crosses combobox
    def populateCrossesCombobox(self,master):
        crosses = self.api.getCrossesDict()
        temp = []

        #append to combobox array
        for i,cross in enumerate(crosses):
            temp.append(f"{cross['base']}/{cross['second']}")

        self.crosses['values'] = temp

    #handle selection of combobox item
    def crossSelected(self, event):
        selected = event.widget.get()
        self.api.setCross(selected)
    
    #plots data
    def plotData(self,master):
        if self.api.getName() == None or self.api.getName() == '':
            mb.showinfo('Notice', 'Select an Currency Cross')
            return
        '''elif self.start_date.get() == None or self.start_date.get() == '':
            mb.showinfo('Notice', 'Enter start date')
            return
        elif self.end_date.get() == None or self.end_date.get() == '':
            mb.showinfo('Notice', 'Enter end date')
            return
        '''

        #check for data in mongo db server
        result = requests.get(f"{const.server}/investing/currency_crosses/get/{self.api.getName()}_{self.api.getCountry()}/{self.start_date.get().replace('/','')}/{self.end_date.get().replace('/','')}",headers=const.headers).json()

        print('Result for getting:', result['data'][0]['data'])

        if result['success'] == 1:
            df = pd.DataFrame(result['data'][0]['data'])
            print('DataFrame: \n', df)

            #drop unnecessary columns
            #TODO: check the original json response
            df.drop(df.columns[[4]], axis=1, inplace=True)

            #draw candles
            const.drawCandles(df, self.api.getName(), self.api.getCountry())
        else: 
            self.updateData()
            self.plotData(master)
    
    #function to update data in database server
    def updateData(self):
        #check for index name and country name
        if self.api.getName() == None or self.api.getName() == "":
            mb.showinfo('Notice', "Select an Currency Cross")
            return

        #get most recent record from server with this name
        data = {
            'currency_name': f"{self.api.getName()}_{self.api.getCountry()}",
        }

        recent = requests.get(f"{const.server}/investing/currency_crosses/get/recent",data=json.dumps(data), headers=const.headers)

        if recent.status_code == 404:
            #get historical data starting from 1980
            self.api.setFromDate('01/01/1980')
            now = datetime.datetime.now()
            self.api.toDate(now.strftime('%d/%m/%Y'))

            historical = self.api.getCrossesData()
            j = json.loads(historical)
            dat = j['historical']

            #send data to mongodb server
            const.saveDataInServer(dat, 'investing/currency_crosses', 'currency_name', self.api)

            mb.showinfo('Notice',f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 200:
            #get recent data
            rec = recent.json()
            print('\n', rec,'\n')

            rec_list = rec['data'][0]['data']
            last_date = rec_list[-1:]
            recent_date = last_date['date']
            print('Recent Date: ', recent_date)
            self.api.setFromDate(recent_date)
            now = datetime.datetime.now()
            self.api.setToDate(now.strftime("%d/%m/%Y"))

            historical = self.api.getCrossesData()
            j = json.loads(historical)
            dat = j['historical']

            #send data to mongo db server
            const.saveDataInServer(dat, 'investing/currency_crosses', 'currency_name', self.api)

            mb.showinfo('Notice', f'Data on {self.api.getName()} updated successfully.')

        elif recent.status_code == 400 or recent.status_code == 500:
            mb.showinfo('Notice', recent.json()['message'])