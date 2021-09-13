import tkinter as tk
import requests


class SearchForSeriesDataflow(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        tk.Label(self,text='Select Indicator For Data Retrieval',width="50").pack(side=tk.TOP)

        #finished building and rendering, create back button
        tk.Button(self,text='Back',command=lambda: self.goBack(master)).pack(side=tk.BOTTOM)

        #initialize local class variables
        self.key = "Dataflow"               #method with series information
        self.series_list = requests.get(f'{master.url}{self.key}').json()\
                        ['Structure']['Dataflows']['Dataflow']
        self.codes_list = []
        self.master = master


        for series in self.series_list:
            if self.master.search_term == None:
                print("Nothing here")
            elif self.master.search_term in series['Name']['#text']:
                print(f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}")

                #search term was found.
                #next, check if code list is available for this series
                #code = re.findall(r'^+\(+\)*$',series['Name']['#text'],flags=re.IGNORECASE)
                code = series['KeyFamilyRef']['KeyFamilyID']
                
                if code != None:
                    print(f'This is code: {code}')
                    #self.master.setIMFDatasetCode(code)

                    self.codes_list.append({"name":f"{series['Name']['#text']}" , "id": f"{series['KeyFamilyRef']['KeyFamilyID']}"})
                    #tk.Button(self,text=f"{series['Name']['#text']}: {series['KeyFamilyRef']['KeyFamilyID']}").pack(side=tk.TOP)
                    #key1 = f'DataStructure/{code}'
                    #dimension_list = requests.get(f'{self.url}{key1}').json()\
                    #                ['Structure']['KeyFamilies']['KeyFamily']\
                    #                ['Components']['Dimension']

                    #for n, dimension in enumerate(dimension_list):
                    #    print(f'Dimension {n+1} {dimension["@codelist"]}')

                    #key2 = f"CodeList/{dimension_list[2]['@codelist']}"
                    #code_list = requests.get(f'{self.url}{key2}').json()\
                    #            ['Structure']['CodeLists']['CodeList']['Code']

                    #for code in code_list:
                    #    print(f"{code['Description']['#text']} : {code['@value']}")
                        
                        #build build buttons for selection of an indicator
                    #    tk.Button(self,text=f"{code['Description']['#text']} : {code['@value']}").pack(side=tk.TOP)
                else: 
                    #the code was not found
                    print('Code was not found in this DataFlow sequence')
            else:
                print(f"{self.master.search_term} could not be found in the Database Structures")

        if self.master.search_term == None:
            tk.Label(self,text=f"Could not find search item : {self.master.search_term}").pack(side=tk.TOP,pady=15)
        elif len(self.codes_list) > 0:
            #create list box with current codes
            scrollbar = tk.Scrollbar(self)
            list = tk.Listbox(self,width="60",height="20")
            scrollbar.config(command=list.yview)
            list.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
            list.pack(side=tk.LEFT,expand=tk.YES,fill=tk.X,pady=15)

            for i,code in enumerate(self.codes_list):
                list.insert(i,code['name'])

            list.config(selectmode=tk.SINGLE,selectbackground="grey")
            list.bind('<Double-1>',self.seriesSelect)
            self.listbox1 = list
        else:     
            tk.Label(self,text=f"Could not find {master.search_tem} in Database Structures").pack(side=tk.TOP,pady=10)

    #function to handle list item click
    def seriesSelect(self,event):
        from imf_select_frequency_frame import SelectFrequencyFrame
        index = self.listbox1.curselection()[0]
        self.master.setIMFDatasetCode(self.codes_list[index]["id"])
        self.master.switch_frame(SelectFrequencyFrame)

    def goBack(self, master):
        from imf_dataset_frame import IMFDataSetFrame
        master.switch_frame(IMFDataSetFrame)
