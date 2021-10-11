'''
    This file contains a class that defines the api for retrieving bonds data from investing.com
'''

import investpy
import tkinter.messagebox as mb
import requests
import json


class BondsAPI:
    def __init__(self, bond=None, country=None, from_date=None, to_date=None):
        self.bond = bond
        self.country = country
        self.from_date = from_date
        self.from_to = to_date

    # get bonds countries
    def getCountries(self):
        countries = investpy.get_bond_countries()
        return countries

    # function to get historical data
    def getBondData(self):
        try:
            data = investpy.get_bond_historical_data(
                bond=self.bond, from_date=self.from_date, to_date=self.to_date, as_json=True)
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

    # function to get recent data
    def getBondRecentData(self):
        try:
            data = investpy.get_bond_recent_data(bond=self.bond, as_json=True)
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

    # function bonds dict
    # return dict
    def getBondsDict(self, country=None, columns=None):
        try:
            bonds = investpy.get_bonds_dict(country=country, columns=columns)
            return bonds
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
    def setBond(self, bond):
        self.bond = bond

    def setCountry(self, country):
        self.country = country

    def setFromDate(self, from_date):
        self.from_date = from_date

    def setToDate(self, to_date):
        self.to_date = to_date

    # defining getters
    def getName(self):
        return self.bond

    def getCountry(self):
        if self.country == None:
            return ""
        else:
            return self.country

    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date
