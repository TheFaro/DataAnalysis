import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id='seven-day-forecast')
forecast_items = seven_day.find_all(class_='tombstone-container')

tonight = forecast_items[2]

print(forecast_items)
print('\n')
#extracting the information we want from tonight variable
period = tonight.find(class_='period-name').get_text()
short_desc = tonight.find(class_='short-desc').get_text()
temp = tonight.find(class_='temp').get_text()

print(period)
print(short_desc)
print(temp)

img = tonight.find('img')
desc = img['title']
print(desc)

#extracting all information from the page
period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
print('\n')
print(periods)
print('\n')

short_descs = [sd.get_text() for sd in seven_day.select('.tombstone-container .short-desc')]
temps = [t.get_text() for t in seven_day.select('.tombstone-container .temp')]
descs = [d['title'] for d in seven_day.select('.tombstone-container img')]


periods.pop(0)
short_descs.pop(0)
descs.pop(0)

print(short_descs)
print(temps)
print(descs)

#combining data into pandas dataframe
weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})

print(weather)

out_file = open('results.txt', 'w')

out_file.write(weather.to_string())
out_file.close()