'''
    This file contains a class to handle data retrieval for the stocks options from investing.com database using investpy module
'''

import investpy
import tkinter.messagebox as mb


class StocksAPI:

    def __init__(self, master, stock=None, country=None, from_date=None, to_date=None):
        self.stock = stock
        self.country = country
        self.from_date = from_date
        self.to_date = to_date

    # get stock company profile
    # returns dictionary
    def getCompanyProfile(self):
        try:

            profile = investpy.get_stock_company_profile(
                stock=self.stock, country=self.country, language='english')
            return profile
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

    # get countries with stocks information available
    # returns list
    def getStockCountries(self):
        countries = investpy.get_stock_countries()
        return countries

    # get stock dividends
    # returns dataframe
    def getStockDividends(self):
        if self.stock != None and self.country != None:
            dividends = investpy.get_stock_dividends(self.stock, self.country)
            return dividends
        else:
            if self.stock != None:
                mb.showinfo('Error', 'Country should be selected.')

            if self.country != None:
                mb.showinfo('Error', 'Stock should be selected.')

    # get stock financial summary
    # returns dataframe
    def getFinancialSummary(self, summary_type='income_statement', period='annual'):
        try:
            summary = investpy.get_stock_financial_summary(
                stock=self.stock, country=self.country, summary_type=summary_type, period=period)
            return summary

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

    # get stock data
    # returns json
    def getStockData(self):
        try:
            # retrieve data to be saved in database.
            data = investpy.get_stock_historical_data(
                stock=self.stock, country=self.country, from_date=self.from_date, to_date=self.to_date, as_json=True)

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

    # gets recent stock data
    def getRecentStockData(self):
        try:
            data = investpy.get_stock_recent_data(
                stock=self.stock, country=self.country, as_json=True)
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

    # get stocks dict
    # returns dict of stocks and their relevant information
    def getStocksDict(self, country=None, columns=None):
        try:
            stocks = investpy.get_stocks_dict(country=country, columns=columns)
            return stocks
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
            else:
                mb.showinfo('Error', 'Unknown error occured.')

    # search for stocks using name, fullname, or isin
    # returns dataframe

    def searchStocks(self, value, by='name'):
        try:
            result = investpy.search_stocks(by=by, value=value)
            return result

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

    def setStock(self, name):
        self.stock = name

    def setCountry(self, name):
        self.country = name

    def setFromDate(self, date):
        self.from_date = date

    def setToDate(self, date):
        self.to_date = date

    # defining getters

    def getName(self):
        return self.stock

    def getCountry(self):
        if self.country == None:
            return ""
        else:
            return self.country

    def getFromDate(self):
        return self.from_date

    def getToDate(self):
        return self.to_date
