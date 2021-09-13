'''
    This file contains a class that defines the api for retrieving commodities data from investing.com
'''

import investpy
import tkinter.messagebox as mb
import requests
import json

class CommoditiesAPI:

    def __init__(self, commodity=None, group=None, from_date=None, to_date=None):
        self.commodity = commodity
        self.group = group
        self.from_date = from_date
        self.to_date = to_date

    #function to retrieve commodity groups
    #returns list
    def getGroups(self):
        groups = investpy.get_commodity_groups()
        return groups

    #function to get historical data about commodities
    #returns json
    def getCommodityData(self):
        try:
            data = investpy.get_commodity_historical_data(commodity=self.commodity, from_date=self.from_date, to_date=self.to_date, as_json=True)
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
        
    #function to get recent data about commodities
    #returns json
    def getCommodityRecentData(self):
        try:
            data = investpy.get_commodity_recent_data(commodity=self.commodity, as_json=True)
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

    #function to get commodities dictionary
    #returns dict
    def getCommoditiesDict(self, group=None,columns=None):
        try: 
            data = investpy.get_commodities_dict(group=group, columns=columns)
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

    #defining setters
    def setCommodity(self, commodity):
        self.commodity = commodity

    def setGroup(self, group):
        self.group = group

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date

    #defining getters
    def getName(self):
        return self.commodity
    
    def getGroup(self):
        return self.group

    def getCountry(self):
        if self.country == None: 
            return ""
        else: 
            return self.country

    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date