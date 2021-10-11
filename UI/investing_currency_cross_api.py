'''
    This file contains a class that defines the api for retrieving currency crosses data from investing.com
'''

import investpy
import tkinter.messagebox as mb


class CrossesAPI:
    def __init__(self, cross=None, from_date=None, to_date=None, country=None):
        self.cross = cross
        self.from_date = from_date
        self.to_date = to_date
        self.country = country

    # function to get currency crosses
    # returns list
    def getCrosses(self):
        crosses = investpy.get_available_currencies()
        return crosses

    # function to get historical data
    # returns json
    def getCrossesData(self):
        try:
            data = investpy.get_currency_cross_historical_data(
                currency_cross=self.cross, from_date=self.from_date, to_date=self.to_date, as_json=True)
            return data
        except (ValueError, FileNotFoundError, IOError, RuntimeError, ConnectionError):
            if ValueError:
                mb.showinfo(
                    'Error', 'Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif IOError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo(
                    'Error', 'Country or Stock does not match any existing data entries.')
            elif ConnectionError:
                mb.showinfo(
                    'Error', 'Could not establish connection to Investing.com')
            else:
                mb.showinfo('Error', 'Unknown error occured.')

    # get recent data
    # returns json
    def getCrossRecentData(self):
        try:
            data = investpy.get_currency_cross_recent_data(
                currency_cross=self.cross, as_json=True)
            return data
        except (ValueError, FileNotFoundError, IOError, RuntimeError, ConnectionError):
            if ValueError:
                mb.showinfo(
                    'Error', 'Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif IOError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo(
                    'Error', 'Country or Stock does not match any existing data entries.')
            elif ConnectionError:
                mb.showinfo(
                    'Error', 'Could not establish connection to Investing.com')
            else:
                mb.showinfo('Error', 'Unknown error occured.')

    # get currency crosses dict
    # returns dict
    def getCrossesDict(self):
        try:
            data = investpy.get_currency_crosses_dict()
            return data
        except(ValueError, FileNotFoundError, IOError, RuntimeError):
            if ValueError:
                mb.showinfo(
                    'Error', 'Check parameters for required data. There may be an error or some values missing.')
            elif FileNotFoundError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif IOError:
                mb.showinfo(
                    'Error', 'File containing required data not found.')
            elif RuntimeError:
                mb.showinfo(
                    'Error', 'Country or Stock does not match any existing data entries.')

    # defining setters
    def setCross(self, cross):
        self.cross = cross

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date

    # defining getters
    def getName(self):
        return self.cross

    def getCountry(self):
        if self.country == None:
            return ""
        else:
            return self.country

    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date
