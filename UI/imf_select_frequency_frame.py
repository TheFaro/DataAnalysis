import tkinter as tk
import requests
import json

from imf_series_dataflow_frame import SearchForSeriesDataflow
import constants as const

class SelectFrequencyFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.chosen_frequency = tk.StringVar()
        
        #build widgets
        #tk.Label(self,text='Choose Data Specifications',height="5",font=("Arial",18)).pack(side=tk.TOP,padx=7)
        tk.Label(self,text='Select Frequency:',font=const.font,width=40).pack(side=tk.TOP)
        self.getDimensions(master)
        self.buildRadioButton(master)
        tk.Button(self,text='Back',command=lambda:master.switch_frame(SearchForSeriesDataflow)).pack(side=tk.BOTTOM,ipady=5,pady=5)
        tk.Button(self,text='Next',command=lambda:self.goToSelectCountry(master)).pack(side=tk.BOTTOM,ipady=5,pady=5)

    #function to build frequency radio buttons
    def buildRadioButton(self,master):

        for i,freq in enumerate(master.frequency_list):
            tk.Radiobutton(
                self,
                text=freq["text"],
                variable=self.chosen_frequency,
                value=freq["code"]).pack(side=tk.TOP,ipady=5)
    
    def goToSelectCountry(self,master):
        from imf_select_countries_frame import SelectCountriesFrame
        print(f"Chosen Freq: {self.chosen_frequency.get()}")
        master.IMF_var.append({"frequency":f"{self.chosen_frequency.get()}"})
        print(master.IMF_var)
    
        #go to the next frame
        print("Go select Countries")
        master.switch_frame(SelectCountriesFrame)


    #function to get the dimensions
    def getDimensions(self,master):
        freq = None
        area = None
        indicator = None
        master.frequency_list = []
        master.country_list = []
        master.indicator_list = []

        key = f'DataStructure/{master.dataset_code}'
        dimension_list = requests.get(f'{master.url}{key}').json()\
                        ['Structure']['KeyFamilies']['KeyFamily']\
                        ['Components']['Dimension']

        for n, dimension in enumerate(dimension_list):
            print(f'Dimension {n+1} {dimension["@codelist"]}')
        
        freq = dimension_list[0]['@codelist']
        area = dimension_list[1]['@codelist']
        indicator = dimension_list[2]['@codelist']

        #get the lists for each of the three paramaters
        for i in range(3):
            if i == 0:
                key2 = f"CodeList/{freq}"
                code_list = requests.get(f'{master.url}{key2}').json()\
                            ['Structure']['CodeLists']['CodeList']['Code']

                for code in code_list:
                    master.frequency_list.append({
                        "text": f"{code['Description']['#text']}", 
                        "code": f"{code['@value']}"
                    })
            
            elif i == 1:
                key2 = f"CodeList/{area}"
                code_list = requests.get(f'{master.url}{key2}').json()\
                            ['Structure']['CodeLists']['CodeList']['Code']

                for code in code_list:
                    master.country_list.append({
                        "text": f"{code['Description']['#text']}",
                        "code": f"{code['@value']}"
                    })
            
            elif i == 2:
                key2 = f"CodeList/{indicator}"
                code_list = requests.get(f'{master.url}{key2}').json()\
                            ['Structure']['CodeLists']['CodeList']['Code']

                for code in code_list:
                    master.indicator_list.append({
                        "text": f"{code['Description']['#text']}",
                        "code": f"{code['@value']}"
                    })