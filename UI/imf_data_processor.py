import requests
import pandas as pd
import json
import constants as const
import tkinter.messagebox as mb


class IMFDataProcessor:
    def __init__(self, master):

        print(len(master.IMF_var))
        print(master.IMF_var[0])
        print(master.IMF_var[1])
        print(master.IMF_var[2])

        # initialize class variables
        self.frequency = master.IMF_var[0]['frequency']
        self.countries = master.IMF_var[1]['country']
        self.indicator = master.IMF_var[2]['indicator']
        self.url = master.url
        self.total_df = None
        self.const = const.Constants()

    def getData(self):
        print(self.total_df)
        #self.total_df = None
        for i, country in enumerate(self.countries):

            query = f'{self.url}CompactData/IFS/{self.frequency}.{country["code"]}.{self.indicator}'
            try:
                data = (requests.get(query).json()
                        ['CompactData']['DataSet']['Series'])

                baseyr = data['@BASE_YEAR']
                self.saveDataInServer(data)

                data_list = [
                    [obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')] for obs in data['Obs']]
                df = pd.DataFrame(data_list, columns=[
                                  'date', f"{country['text']}"])

                df = df.set_index(pd.to_datetime(df['date']))[
                    f"{country['text']}"].astype('float')

                if i == 0:
                    self.total_df = df.to_frame()
                elif i > 0:
                    self.total_df = pd.merge(
                        self.total_df, df, how='outer', on='date', left_index=True)
            except KeyError:
                print(f"There is no data for {country['text']}")

    # function to handle checking for data in mongodb server
    def getIMFDataFromServer(self):
        print(self.total_df)
        self.total_df = None
        # check for data in server
        if self.indicator != None:
            for i, country in enumerate(self.countries):

                try:
                    result = requests.get(
                        f"{self.const.server}/imf/get/{self.indicator}/{country['code']}", headers=self.const.headers)

                    if result.status_code == 200:  # Status OK!
                        # data was found
                        data = (result.json()['Series'])

                        data_list = [
                            [obs.get("@TIME_PERIOD"), obs.get('@OBS_VALUE')] for obs in data['Obs']]
                        df = pd.DataFrame(data_list, columns=[
                                          'date', f"{country['text']}"])

                        df = df.set_index(pd.to_datetime(df['date']))[
                            f"{country['text']}"].astype('float')
                        if i == 0:
                            self.total_df = df.to_frame()
                        elif i > 0:
                            self.total_df = pd.merge(
                                self.total_df, df, how='outer', on='date', left_index=True)

                    elif result.status_code == 404:
                        # not found in database.
                        # retrieve data from api
                        self.getData()
                    elif result.status_code == 400 and result.status_code == 500:
                        mb.showinfo('Notice', result.json['message'])
                except KeyError:
                    print('Something is an error in [getIMFDataFromServer]')

    # function to handle saving dataset in mongodb server
    def saveDataInServer(self, series):
        data = {
            'Series': series
        }

        result = requests.post(f"{self.const.server}/imf/create",
                               data=json.dumps(data), headers=self.const.headers)

        print(result.json())
