#local module imports
from menu import *                          #local module that has the menu definition root

#system module imports
import tkinter as tk
from tkinter import ttk as TTK
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import re
import json

#third party modules
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import requests

class App(tk.Tk):
    
    def __init__(self):
        #using the super class Tkinter constructor
        tk.Tk.__init__(self)                
        
        #class variable
        self._frame = None                              #current frame showing
        self.mFilePath = None                           #current chosen file paths
        self.mChosenSheet = None                        #current sheet chosen in workbook
        self.search_term = None                         #current IMF search string
        self.dataset_code = None                        #current IMF dataset code 
        self.url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/"
        self.IMF_var = []                               #stores resulting IMF variables for data retrieval
        self.frequency_list = []
        self.country_list = []
        self.indicator_list = []

        #inflating initial frame
        self.switch_frame(MenuFrame)

    #function definition to switch frames
    def switch_frame(self, frame_class):
        #assign frame class parameter to local variable
        new_frame = frame_class(self)

        #destroy the current from if it exists
        if self._frame is not None:
            print("Destroyed: %s" % (self._frame.winfo_class))
            self._frame.destroy()
        elif new_frame is not None:
            print("New frame: %s" % (new_frame.winfo_class))

        #assign the new frame to the class frame variable
        self._frame = new_frame
        self._frame.pack()
    
    #function to store the workbook file path on selection
    def setFilePath(self, path):
        self.mFilePath = path
    
    def getFilePath(self, path):
        return self.mFilePath

    #function to store the sheet a user has selected from the workbook
    def setChosenSheet(self,name):
        self.mChosenSheet = name   

    #function to store IMF search string
    def setIMFSearchString(self,search):

        if search == "":
            self.search_term = None
        else:
            self.search_term = search

    #function to store IMF dataset code 
    def setIMFDatasetCode(self,code):
        self.dataset_code = code


class MenuFrame(tk.Frame):
    def __init__(self, master):
        #call the super class Frame constructor
        tk.Frame.__init__(self, master)

        #definition of frame widgets and their functionality
        #definition of the view charts button
        self.viewBtn = tk.Button(self,text='View Charts[Offline]',command=lambda: master.switch_frame(SelectFileFrame))
        self.viewBtn.pack(pady=20,ipadx=120,ipady=5)
        
        #definition of update data button
        self.updateBtn = tk.Button(self,text='View Charts[Online]',command=lambda:master.switch_frame(ChooseDataSourceFrame))
        self.updateBtn.pack(pady=20,ipadx=120,ipady=5)
        
        #definition of the exit button
        self.exitBtn = tk.Button(self,text='Exit',command=self.quit)
        self.exitBtn.pack(pady=12,ipadx=60,ipady=5)

##################### OFFLINE DEFINITIONS ###############################

class SelectFileFrame(tk.Frame):
    def __init__(self,master):
        #call super class Frame constructor
        tk.Frame.__init__(self,master)

        #class variable to store the file path to display on label
        self.filename = tk.StringVar()

        #to handle back pressed from SelectSheet class
        if master.mFilePath == None: 
            self.filename.set('No file selected.')
        else: 
            self.filename.set(master.mFilePath)

        #build widgets for this frame

        #button to open the file from the Operating system
        self.openBtn = tk.Button(self,text='Open File',command=lambda: self.openFilePath(master))
        self.openBtn.pack(pady=12,ipadx=60,ipady=5)

        #label to display the path to the file
        self.filepath = tk.Label(self,textvariable=self.filename)
        self.filepath.config(bg='white',fg='black')
        self.filepath.pack(pady=12, ipadx=60, ipady=5)

        
        #next button to continue with the process
        self.nextBtn = tk.Button(self,text='Next',command=lambda: master.switch_frame(SelectSheet))
        self.nextBtn.pack(pady=50, ipadx=20,ipady=5,side=tk.RIGHT)

        #back button
        self.backBtn = tk.Button(self,text='Back',command=lambda: master.switch_frame(MenuFrame))
        self.backBtn.pack(pady=20, ipadx=20,ipady=5,side=tk.RIGHT)
            

    #function to retrieve the file to be opened
    def openFilePath(self, master):
        filepath = fd.askopenfilename(filetypes = [('Excel Files', '*.xlsm'),('Excel Files', '*.xlsx'), ('All Files','*.*')])

        if filepath is not None:

            #set the filename to display on the label
            self.filename.set(filepath)

            #set the root class file path variable
            master.setFilePath(filepath)


class SelectSheet(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        #class variables
        self.mBook = xlrd.open_workbook(master.mFilePath)   #hold the recently opened workbook
        self.BookList = self.mBook.sheets()    

        #loop that builds the buttons to display the sheet names
        for i in range(0, len(self.mBook.sheets())) :
            Button = tk.Button(self,text=self.BookList[i].name,command=lambda i=i: self.buttonClick(master,i))
            Button.pack()

        #defining a back button
        tk.Button(self,text='Back',command=lambda: master.switch_frame(SelectFileFrame),fg='white',bg='black').pack(pady=20)
    
    #function to handle button click
    def buttonClick(self, master,index):
        if index != None:
            self.chosenName(master,self.BookList[index])
        else: 
            print("There is an error")

    def chosenName(self, master, name):
        master.setChosenSheet(name)
        print(master.mChosenSheet.name)
        master.switch_frame(ShowColumnsFrame(master))
    
    def __call__(self, master):
        SelectSheet(master).pack()


class ShowColumnsFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text=master.mChosenSheet.name).pack()
        

        #class variables
        self.states = []
        self.columnHeads = []
        self.selectedColumns = []
        self.rowStart = None
        self.columnStart = None
        self.entire_sheet = pd.read_excel(master.mFilePath,master.mChosenSheet.name,index_col=None,header=None).fillna(0.0)
        self.df = None

        self.getRelationColumns(master)
        self.buildCheckboxes()

        #build back button
        tk.Button(self,text='<- Back',command=lambda:self.goBack(master)).pack()
        
        #build selected fields button
        tk.Button(self,text='Selected fields',command=self.showSelectedFields).pack()
        
        #next button
        tk.Button(self,text='Next',command=self.add_to_dataframe).pack()

    def goBack(self, master):
        self.destroy()
        master.switch_frame(SelectSheet)

    def showSelectedFields(self):
        mb.showinfo(self.selectedColumns.count)
        print(self.selectedColumns)

    def __call__(self, master):
        ShowColumnsFrame(master).pack()

    def getRelationColumns(self, master):
        tmpSheet = master.mChosenSheet
        tmpRow = None
        for i in range(0, tmpSheet.nrows):
            for j in range(0, tmpSheet.ncols):
                #print(tmpSheet.cell(i,j).value)
                
                tmpCell = tmpSheet.cell(i, j)  
                #print tmpCell

                if tmpCell.ctype == 1 :
                    if tmpCell.value == "Date/Symbol":
                        tmpRow = i
                        self.rowStart = i
                        self.columnStart = j


                    if tmpRow == i: 
                        self.columnHeads.append(tmpCell.value)


        
    def buildCheckboxes(self):
        sbar = tk.Scrollbar(self)
        list = tk.Listbox(self, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT,fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
    
        for i in range(len(self.columnHeads)):
            list.insert(i, self.columnHeads[i])
        
        list.config(selectmode=SINGLE,setgrid=1)
        list.bind('<Double-1>',self.handleList)
        self.listbox = list

    def handleList(self,event):
        index = self.listbox.curselection()
        label = self.listbox.get(index)

        print('You have added: %s to the list' % (label))
        #mb.showinfo(('You have added: ',label,'to the list'))
        
        #add clicked item to class list variable
        self.selectedColumns.append(index[0])
        print(self.selectedColumns)

    def add_to_dataframe(self):
        dataFrame = pd.DataFrame({})
        for icol in self.selectedColumns:
            series = None
            dataList = []
            tempName = None
            for irow in range(self.rowStart,len(self.entire_sheet)):
                if(irow == self.rowStart):
                    tempName = self.entire_sheet.iloc[irow][icol]
                dataList.append(self.entire_sheet.iloc[irow][icol])

            #series = pd.Series(dataList,name=tempName)
            #print series
            dataList.pop(0)
            dataFrame[tempName] = dataList
        
        self.df = dataFrame

        #melted = pd.melt(self.df,id_vars=['Date/Symbol'])
        #print(self.df)
        for key,values in self.df.iteritems():
            print("%s %s" % (key, values))
            if key != 'Date/Symbol':
                self.df[key] = self.df[key].astype(float)
        #self.df.plot(x ='Date/Symbol',kind='line')
        #plt.show()
        self.df.set_index('Date/Symbol',verify_integrity=True)
        print(self.df)
        ax = sb.lineplot(data=self.df)
        ax.set(xlabel="Date",ylabel="Symbol")
        plt.show()


########################### ONLINE DEFINITIONS ##############################

class ChooseDataSourceFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master)

        #class variables
        self.data_sources = []

        #add IMF as a data source
        self.data_sources.append('International Monetary Fund (IMF) Database')

        #build Button to select and facilitate data source
        for i in range(0, len(self.data_sources)):
            Button = tk.Button(self,text=self.data_sources[i],command=lambda i=i: self.buttonClick(master,i))
            Button.pack()

        #definition of back button
        tk.Button(self,text='Back',command=lambda:master.switch_frame(MenuFrame),fg='white',bg='black').pack()

    #handle button click on data source
    def buttonClick(self, master, index):
        if index != None: 
            #go to next frame
            #frame lists DataFlows or DataSets found in IMF Database/Data source
            master.switch_frame(SelectDataSetFrame)


########################## IMF Data source selected ###############################
class SelectDataSetFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        self.sets_list = []
        self.master = master

        #add data sets to the list
        '''self.sets_list.append({"code": "FSI","name": "Financial Soundness Indicators"})
        self.sets_list.append({"code": "FAS","name": "Financial Access Survey"})
        self.sets_list.append({"code": "IFS","name": "International Financial Statistics"})
        self.sets_list.append({"code": "MCDREP","name": "Middle East and Central Asia Regional Economic Outlook"})
        self.sets_list.append({"code": "DOTS","name": "Direction of Trade Statistics"})
        self.sets_list.append({"code": "CDIS","name": "Coordinated Direct Investment Survey"})
        self.sets_list.append({"code": "GFS","name": "Government Finance Statistics"})
        self.sets_list.append({"code": "BOP","name": "Balance Of Payments"})
        self.sets_list.append({"code": "CPIS","name": "Coordinated Portfolio Investment Survey"})
        self.sets_list.append({"code": "APDREO","name": "Asia and Pacific Regional Economic Outlook"})
        self.sets_list.append({"code": "FM","name": "Fiscal Monitor"})
        self.sets_list.append({"code": "AFRREO","name": "Sub-Saharan Africa Regional Economic Outlook"})
        self.sets_list.append({"name": "Primary Commodity Prices"})
        self.sets_list.append({"code": "WoRLD","name": "World Revenue Longitudinal Data"})
        self.sets_list.append({"code": "PGI","name": "Principal Global Indicators"})
        self.sets_list.append({"code": "WHDREO","name": "Western Hemisphere Regional Economic Outlook"})
        self.sets_list.append({"code": "WCED","name": "World Commodity Exports"})
        self.sets_list.append({"code": "ICSD","name": "Investment and Capital Stock"})
        self.sets_list.append({"code": "HPDD","name": "Historical Public Debt"})
        self.sets_list.append({"code": "COFR","name": "Coverage of Fiscal Reporting"})
        self.sets_list.append({"code": "CPI","name": "Consumer Price Index"})
        self.sets_list.append({"code": "IRFCL","name": "International Reserves and Foriegn Currency Liquidity"})
        self.sets_list.append({"code": "COFER","name": "Currency Composition Of Official Foreign Exchange Reserves"})
        self.sets_list.append({"code": "MFS","name": "Monetary and Financial Statistics"})
        self.sets_list.append({"code": "SNA","name": "System of National Accounts"})'''

        #create widgets
        self.search_text = tk.StringVar()
        self.search_text.set("IMF - DataSets")
        title = tk.Label(self,textvariable=self.search_text,width="40").pack(side=tk.TOP)

        #search bar
        edit = tk.Entry(self)
        edit.pack(side=tk.TOP, fill=BOTH, expand=1)
        edit.focus_set()

        #add search button
        search_button = tk.Button(self, text='Search',command=lambda:self.setSearchTerm(edit.get())).pack(side=tk.TOP,pady=15)

        #add get all button
        get_all_button = tk.Button(self,text='Get All Data Sets',command=lambda:self.getAll()).pack(side=tk.TOP,pady=10)

        #define a back button
        back_button = tk.Button(self,text="Back",command=lambda:self.master.switch_frame(ChooseDataSourceFrame))
        back_button.pack(side=tk.BOTTOM,pady=15)

        #create a list box with current dataset list 
        '''scrollbar = tk.Scrollbar(self)
        list = tk.Listbox(self,relief=SUNKEN,width="60",height="20")
        scrollbar.config(command=list.yview)
        list.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT,fill=Y)
        list.pack(side=tk.LEFT, expand=YES, fill=X,pady=15)

        for i in range(len(self.sets_list)):
            list.insert(i, self.sets_list[i]["name"])
            
        list.config(selectmode=SINGLE,setgrid=1)
        list.bind('<Double-1>', self.selectedDataset)
        self.list_box = list'''

    #function that retrieves selected dataset code
    def selectedDataset(self,event):
        index = self.list_box.curselection()
        idx = index[0]
        print('Selected DataSet: ', self.sets_list[idx]['code'])

        #set selected dataset code
        self.master.setIMFDatasetCode(self.sets_list[idx]['code'])
    
    #function to set search term
    def setSearchTerm(self, term):
        self.master.setIMFSearchString(term)
        print("Search text: %s" % self.master.search_term)
        self.master.switch_frame(SearchForSeriesDataflow)

    #function to get all datasets
    def getAll(self):
        self.master.search_term = ""
        print("Iam here")
        self.master.switch_frame(SearchForSeriesDataflow)

#class to handle searching of series list for searched string
class SearchForSeriesDataflow(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        tk.Label(self,text='Select Indicator For Data Retrieval',width="50").pack(side=tk.TOP)

        #finished building and rendering, create back button
        tk.Button(self,text='Back',command=lambda: master.switch_frame(SelectDataSetFrame)).pack(side=tk.BOTTOM)

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
            scrollbar.pack(side=tk.RIGHT,fill=Y)
            list.pack(side=tk.LEFT,expand=YES,fill=X,pady=15)

            for i,code in enumerate(self.codes_list):
                list.insert(i,code['name'])

            list.config(selectmode=SINGLE,selectbackground="grey")
            list.bind('<Double-1>',self.seriesSelect)
            self.listbox1 = list
        else:     
            tk.Label(self,text=f"Could not find {master.search_tem} in Database Structures").pack(side=tk.TOP,pady=10)

    #function to handle list item click
    def seriesSelect(self,event):
        index = self.listbox1.curselection()[0]
        print(self.codes_list[index]["id"])
        self.master.setIMFDatasetCode(self.codes_list[index]["id"])
        self.master.switch_frame(SelectFrequencyFrame)


#class to handle selection of frequency, area code and indicator
class SelectFrequencyFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.chosen_frequency = tk.StringVar()
        
        #build widgets
        #tk.Label(self,text='Choose Data Specifications',height="5",font=("Arial",18)).pack(side=tk.TOP,padx=7)
        tk.Label(self,text='Select Frequency:',font=('Arial Bold',12),width="40").pack(side=tk.TOP)
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


#Frame to select the countries to be displayed and plotted for comparision
class SelectCountriesFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.count_var = tk.StringVar()
        
        try:
            if len(master.IMF_var[1]['country']) > 0:
                print(" I am first")
                self.select_list = master.IMF_var[1]['country']
                print(self.select_list)
            else:
                print("I am second")
                self.select_list = []
        except (KeyError,IndexError): 
            print('I am in error')
            self.select_list = []

        #show countries in combobox
        tk.Label(self,text='Select Countries from list below',font=('Arial Bold', 18)).pack(side=tk.TOP)
        self.countries = TTK.Combobox(self,width = 27,textvariable=self.count_var)
        self.populateCombobox(master)
        self.countries.pack(side=tk.TOP)
        self.countries.current(0)
        self.createListbox(master)

        #create buttons
        tk.Button(self,text="Back",command=lambda:self.back(master)).pack(side=tk.TOP)
        tk.Button(self,text="Add Country to List",command=lambda:self.addToSelectedList(master)).pack(side=tk.TOP)
        tk.Button(self,text="Next",command=lambda:self.next(master)).pack(side=tk.TOP)
        
    def next(self,master):      
        if len(self.select_list) == 0:
            print("No country selected. Please select one.")
            mb.showinfo('No Country Selected. Please select at least one.')
        
        else:
            master.IMF_var.append({'country': self.select_list})
            master.switch_frame(SelectIndicatorsFrame)

    def back(self,master):
        master.switch_frame(SelectFrequencyFrame)

    def populateCombobox(self,master):
        temp = []

        for i,country in enumerate(master.country_list):
            temp.append(country['text'])

        self.countries['values'] = temp

    def addToSelectedList(self,master):
        for i,count in enumerate(master.country_list):
            if self.count_var.get() == count['text']:
                #add country code to selected list
                self.select_list.append(count)

                #add to listbox 
                self.addToListbox(i,count['text'])

    def createListbox(self,master):
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self,width="60",height="20")
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT,fill=Y)
        self.listbox.pack(side=tk.LEFT,expand=YES,fill=tk.X,pady=15)
        self.listbox.config(selectmode=SINGLE,selectbackground='grey')
        self.listbox.bind('<Double-1>',self.deleteFromListbox)

        if len(self.select_list) > 0:
            for i,country in enumerate(self.select_list):
                self.listbox.insert(i,country['text'])

    def addToListbox(self, index, value):
        self.listbox.insert(index,value)

    def deleteFromListbox(self,event):
        print(self.select_list)
        idx = self.listbox.curselection()[0]
        #todo - use delete function to remove clicked item
        self.listbox.delete(idx)
        del self.select_list[idx]
        print(self.select_list)

class SelectIndicatorsFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        self.master = master

        #create listbox to display indicators and handle click on one
        self.scrollbar = tk.Scrollbar(self)
        self.listbox = tk.Listbox(self,width="60",height="20")
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT,fill=Y)
        self.listbox.pack(side=tk.LEFT,expand=YES,fill=tk.X,pady=15)
        self.listbox.config(selectmode=SINGLE,selectbackground='grey')
        self.listbox.bind('<Double-1>',self.getDataFromDataSource)
        
        for i,indicator in enumerate(self.master.indicator_list):
            self.listbox.insert(i,indicator['text'])
        
        tk.Button(self,text='Back',command=lambda:master.switch_frame(SelectCountriesFrame)).pack(side=tk.TOP)

    def getDataFromDataSource(self,event):
        index = self.listbox.curselection()[0]
        print(self.master.indicator_list[index]["code"])
        if len(self.master.IMF_var) < 3:
            self.master.IMF_var.append({'indicator': f'{self.master.indicator_list[index]["code"]}'})
        else:   
            self.master.IMF_var[2] = {'indicator': f'{self.master.indicator_list[index]["code"]}'}
        print(self.master.IMF_var[2])
        
        data_processor = IMFDataProcessor(self.master)
        data_processor.getData()
        print(data_processor.total_df)
        
        if data_processor.total_df.empty == False:
            ax = sb.lineplot(data=data_processor.total_df)
            ax.set(xlabel="Date",ylabel="Symbol")
            plt.show()
        else: 
            print('No data available for plotting')            

class IMFDataProcessor:
    def __init__(self, master):

        print(len(master.IMF_var))
        print(master.IMF_var[0])
        print(master.IMF_var[1])
        print(master.IMF_var[2])

        #initialize class variables
        self.frequency = master.IMF_var[0]['frequency']
        self.countries = master.IMF_var[1]['country']
        self.indicator = master.IMF_var[2]['indicator']
        self.url       = master.url
        self.total_df  = None

    
    def getData(self):
        print(self.total_df)
        for i,country in enumerate(self.countries):
            
            query = f'{self.url}CompactData/IFS/{self.frequency}.{country["code"]}.{self.indicator}'
            try: 
                data = (requests.get(query).json()
                    ['CompactData']['DataSet']['Series'])
                
                baseyr = data['@BASE_YEAR']

                data_list = [[obs.get('@TIME_PERIOD'),obs.get('@OBS_VALUE')] for obs in data['Obs']]
                df = pd.DataFrame(data_list, columns=['date',f"{country['text']}"])

                df = df.set_index(pd.to_datetime(df['date']))[f"{country['text']}"].astype('float')

                if i == 0:
                    self.total_df = df.to_frame()
                elif i > 0:
                    self.total_df = pd.merge(self.total_df,df,how='outer',on='date',left_index=True)
            except KeyError:
                print(f"There is no data for {country['text']}")

    #def plotGraphs(self):
        #see from internet how to plot multiple graphs with pandas and matplotlib

#This is the start of the main function
if __name__ == "__main__":
    app = App()
    app.title('Data Collecting and Chart Viewer Tool')
    makemenu(app)
    app.mainloop()