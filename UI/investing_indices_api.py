'''
    This file contains a class that defines the api for retrieving indices data from investing.com
'''

import investpy
import tkinter.messagebox as mb

class IndicesAPI:
    def __init__(self, indices=None, country=None, from_date=None, to_date=None):
        self.indices = indices
        self.country = country
        self.from_date = from_date
        self.to_date = to_date
    
    #get countries
    #returns list
    def getIndicesCountries(self):
        countries = investpy.get_index_countries()
        return countries

    #get historical data
    #returns json
    def getIndexData(self):
        try:
            data = investpy.get_index_historical_data(index=self.indices, country=self.country, from_date=self.from_date, to_date=self.to_date, as_json=True)
            return data
        except (ValueError, FileNotFoundError, IOError, RuntimeError, ConnectionError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')
            elif ConnectionError:
                mb.showinfo('Error', 'Could not establish connection to Investing.com')
            else:
                mb.showinfo('Error', 'Unknown error occured.')
        
    #get recent index data
    #returns json
    def getRecentIndexData(self):
        try:
            data = investpy.get_index_recent_data(index=self.indices,country=self.country,as_json=True)
            return data
        except (ValueError, FileNotFoundError, IOError, RuntimeError, ConnectionError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')
            elif ConnectionError:
                mb.showinfo('Error', 'Could not establish connection to Investing.com')
            else:
                mb.showinfo('Error', 'Unknown error occured.')

    #get indices dict
    #returns dict
    def getIndicesDict(self, country=None, columns=None):
        try: 
            indices = investpy.get_indices_dict(country=country, columns=columns)
            return indices
        except(ValueError, FileNotFoundError, IOError, RuntimeError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')

    #defining setter
    def setIndex(self, index):
        self.indices = index

    def setCountry(self, country):
        self.country = country

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date

    #defining getters
    def getName(self):
        return self.indices
    
    def getCountry(self):
        if self.country == None:
            return ""
        else:
            return self.country
    
    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date