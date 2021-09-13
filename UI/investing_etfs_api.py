'''
    This file contains a class that defines the api for retrieving etf data from investing.com
'''

import investpy
import tkinter.messagebox as mb
import requests
import json

class ETFSAPI:
    def __init__(self,etfs=None,country=None,from_date=None,to_date=None):
        self.etfs = etfs
        self.country = country
        self.from_date = from_date
        self.to_date = to_date

    #get countries with etfs information
    #returns list
    def getEtfsCountries(self):
        countries = investpy.get_etf_countries()
        return countries
    
    #get historical etfs data
    #returns json
    def getEtfData(self):
        try:
            data = investpy.get_etf_historical_data(etf=self.etfs, country=self.country, from_date=self.from_date, to_date=self.to_date,as_json=True)
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

    #get recent etf data
    #returns json
    def getRecentEtfData(self):
        try:
            data = investpy.get_etf_recent_data(etf=self.etfs,country=self.country, as_json=True)
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

    #get etfs dict
    #returns dict
    def getEtfsDict(self, country=None, columns=None):
        try:
            etfs = investpy.get_etfs_dict(country=country, columns=columns)
            return etfs
        except(ValueError, FileNotFoundError, IOError, RuntimeError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')

    #defining setters
    def setEtfs(self, etf):
        self.etfs = etf

    def setCountry(self, country):
        self.country = country

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date


    #defining getters
    def getName(self):
        return self.etfs

    def getCountry(self):
        if self.country == None:
            return ""
        else:
            return self.country

    def getFromCountry(self):
        return self.from_date

    def getToDate(self):
        return self.to_date