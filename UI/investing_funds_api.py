'''
    This file contains a class that defines the api for retrieving funds data from investing.com
'''

import investpy
import tkinter.messagebox as mb
import requests
import json

class FundsAPI:

    def __init__(self, master, fund=None, country=None, from_date=None, to_date=None):
        self.fund = fund
        self.country = country
        self.from_date = from_date
        self.to_date = to_date

    #get countries with funds information
    #returns list
    def getFundsCountries(self):
        countries = investpy.get_fund_countries()
        return countries

    #get historical funds data
    #returns json
    def getFundData(self):
        try:
            data = investpy.get_fund_historical_data(fund=self.fund, country=self.country, from_date=self.from_date, to_date=self.to_date)
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

    #get recent funds data
    #returns json
    def getRecentFundData(self):
        try:
            data = investpy.get_fund_recent_data(fund=self.fund, country=self.country)
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

    #get funds dict
    #return dict of funds
    def getFundsDict(self, country=None, columns=None):
        try:
            funds = investpy.get_funds_dict(country=country, columns=columns)
            return funds
        except(ValueError, FileNotFoundError, IOError, RuntimeError):
            if ValueError:
                mb.showinfo('Error','Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo('Error', 'File containing required data not found.')
            elif IOError: 
                mb.showinfo('Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo('Error', 'Country or Stock does not match any existing data entries.')

    ## defining setters.
    def setFund(self, fund):
        self.fund = fund

    def setCountry(self, country):
        self.country = country

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date
    
    ## defining getters
    def getName(self):
        return self.fund
    
    def getCountry(self):
        if self.country == None:
            return ""
        else: 
            return self.country

    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date