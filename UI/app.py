import tkinter as tk

from menu_frame import *

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

        self.width = self.winfo_screenwidth() 
        self.height = self.winfo_screenheight()

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
