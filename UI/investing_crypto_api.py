'''
    This file contains a class that defines the api for retrieving crypto currency data from investing.com
'''

import investpy
import tkinter.messagebox as mb

class CryptoAPI:
    def __init__(self, crypto=None, from_date=None, to_date=None):
        self.crypto = crypto
        self.from_date = from_date
        self.to_date = to_date

    #get cyrpto currency dict
    #returns dict
    def getCryptoDict(self):
        try:
            data = investpy.get_cryptos_dict()
            return data
        except(ValueError, FileNotFoundError, IOError, RuntimeError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')
    
    #get cryptos historical data
    #returns json
    def getCryptoData(self):
        try: 
            data = investpy.get_crypto_historical_data(crypto=self.crypto,from_date=self.from_date,to_date=self.to_date, as_json=True)
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
        
    #gets recent cryptos data
    #return json
    def getCryptosRecentData(self):
        try:
            data = investpy.get_cryptos_recent_data(crypto=self.crypto, as_json=True)
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

    #defining setters
    def setCrypto(self, crypto):
        self.crypto = crypto

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date
    
    #defining getters
    def getName(self):
        return self.crypto

    def getCountry(self):
        if self.country == None:
            return ""
        else: 
            return self.country

    def getFromDate(self):
        return self.from_date
    
    def getToDate(self):
        return self.to_date