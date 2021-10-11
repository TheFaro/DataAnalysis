import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpdates
import requests
import json
import seaborn as sb


class Constants:

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
        }

        self.server = 'http://localhost:8080'

        self.font = ('Arial', 12, 'bold')
        self.title_font = ('Arial', 14, 'bold')
        self.hint_font = ('Arial', 10, 'italic')

    # handles plotting candles
    # the dataframe has been cleaned and can be used for plotting
    def drawCandles(self, df, title_name, country_name):
        # convert into datetime object
        df['date'] = pd.to_datetime(df['date'])

        # apply map function
        df['date'] = df['date'].map(mpdates.date2num)

        # creating subplots
        fig, ax = plt.subplots()

        # plotting the data
        candlestick_ohlc(ax, df.values, width=0.6,
                         colorup='green', colordown='red', alpha=0.8)

        # allow grid
        ax.grid(True)

        # setting labels
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')

        # setting title
        plt.title(f'{title_name}_{country_name} data')

        # formatting date
        date_format = mpdates.DateFormatter("%d-%m-%Y")
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()

        # show plot
        plt.show()

    # handles plotting line graphs
    def drawLineGraph(self, df, title_name):
        # convert date to datetime object
        df['date'] = pd.to_datetime(df['date'])

        # apply map function
        df['date'] = df['date'].map(mpdates.date2num)

        sb.lineplot(x=df['date'], y=df[''], data=df, )
        plt.show()

    # function to add data into node server in steps of one hundred each
    def saveDataInServer(self, data, path_name, json_name, entity_class):
        print(f'In save server', data)
        # first have a temporary list to input the current 100 values
        temp = []

        # a counter to keep track of the number of entries in the temporary array
        counter = 0

        # a variable to keep the last data list number read
        last_entry_read = 0
        self.last_entry_read = 0
        # a boolean variable to indicate when finished
        done = False

        while(done == False):
            try:
                last_entry_read = self.last_entry_read
                temp = []

                # for each item from the last entry read to plus 100
                for item in range(last_entry_read, last_entry_read+99):
                    temp.append(data[item])
                    print('last: ', self.last_entry_read,)
                    self.last_entry_read += 1

                print('This is temp, Here is temp', temp)

                # send the 100 items to the server
                if self.last_entry_read == 0:
                    # create new instance when sending data to server
                    data = {
                        json_name: f"{entity_class.getName()}_{entity_class.getCountry()}",
                        'data': temp
                    }

                    print('First run data', counter, json.dumps(data))

                    result = requests.post(
                        f'{self.server}/{path_name}/create', data=json.dumps(data), headers=self.headers).json()
                    print("Result", result)

                    if result['success'] == 0:
                        print('There was a problem in count', counter)
                        print(result['message'])
                    # update last entry read
                    counter = counter + 1
                elif self.last_entry_read > 0:
                    # update the exitsing instance data
                    data = {
                        json_name: f"{entity_class.getName()}_{entity_class.getCountry()}",
                        'data': temp
                    }

                    print('Not First data', counter, json.dumps(data))
                    result = requests.put(
                        f'{self.server}/{path_name}/update', data=json.dumps(data), headers=self.headers)
                    print('Result', result)

                    # update last entry read
                    counter = counter + 1
                else:
                    print('Neither of the above')

            except (IndexError, KeyError):
                print('The last item has been read')
                if len(data)-1 == self.last_entry_read:
                    done = True

                print('Send the current data to the server')
                data = {
                    json_name: f"{entity_class.getName()}_{entity_class.getCountry()}",
                    'data': temp
                }

                print('data', counter, json.dumps(data))
                result = requests.put(
                    f'{self.server}/{path_name}/update', data=json.dumps(data), headers=self.headers).json()
                print('result', result)
