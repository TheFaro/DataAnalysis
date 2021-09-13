import requests
import pandas as pd
import matplotlib.pyplot as plt
import json as J

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
key = 'CompactData/IFS/M.GB.PCPI_IX'

#Navigate to series in API returned JSON data
data = (requests.get(f'{url}{key}').json()
        ['CompactData']['DataSet']['Series'])

#print(data)      #print latest observation

outfile = open("imf/cpi_Utilities.json","w+")
outfile.write(J.dumps(requests.get(f'{url}{key}').json()))
outfile.close()

baseyr = data['@BASE_YEAR']     #save the base year

#create pandas dataframe from the observations 
data_list = [[obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')] for obs in data['Obs']]

df = pd.DataFrame(data_list, columns=['date', 'value'])
print(df)

df = df.set_index(pd.to_datetime(df['date']))['value'].astype('float')

#save cleaned dataframe as a csv file
df.to_csv('UK_gdp.csv', header=True)

#title and text with recent value
title = f'U.K. Import Prices (index,{baseyr})'
recentdt = df.index[-1].strftime('%B %Y')
recentval = round(df[-1],1)
recent = f'Most recent: {recentdt}: {recentval}'
source = 'Source: IMF IFS'

#basic plot
plot = df.plot(title=title, colormap='Set1')
plot = plot.set_xlabel(f'{recent}; {source}')
plt.show()