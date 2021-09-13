import requests
import pandas as pd

url = 'http://dataservices.img.org/REST/SDMX_JSON.svc/'
key = 'GenericMetadata/IFS/M.GB.PMP_IX'

metadata = requests.get(f'{url}{key}').json()
country = metadata['GenericMetadata']['MetadataSet']\
        ['AttributeValueSet'][1]['ReportedAttribute']\
        [1]['ReportedAttribute'][3]['Value']['#text']

indicator = metadata['GenericMetadata']['MetadataSet']\
        ['AttributeValueSet'][2]['ReportedAttribute']\
        [1]['ReportedAttribute'][4]['Value']['#text']

print(f'Country: {country}; Indicator: {indicator}')


#more complex requests
#key includes two partners, B0 and W00 for EU and the World
key = 'CompactData/DOT/M.GB.TMG_CIF_USER.B0+W00'

#Retrieve data from the IMF API
data = requests.get(f'{url}{key}').json()

#Convert results into pandas dataframe
df = pd.DataFrame(s{['@COUNTERPART_AREA'] : {pd.to_datetime(i['@TIME_PERIOD']) :
        round(float(i['@OBS_VALUE']),1) for i in s['Obs']}
        for s in data['CompatData']['DataSet']['Series']})

#12 month moving average of EU share of total
eu_share = (df['B0'].div(df['W00']) * 100).rolling(12).mean()

#Create a line plot and print most recent value as x label
title = "U.K. imports of goods: European Union share of total"
recent = f"{eu_share.index[-1].strftime('%B %Y')}: {eu_share[-1].round(1)}%"
ax = eu_share.plot(title=title)
ax = ax.set_xlabel(recent)