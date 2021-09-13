import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.X_sbKK5S_eQ')
soup = BeautifulSoup(page.content, 'html.parser')

detailed_list = soup.find(id='detailed-forecast')
labels = [l.get_text() for l in detailed_list.select(".forecast-label")]
texts = [t.get_text() for t in detailed_list.select(".forecast-text")]

print(labels)

df = pd.DataFrame({
    "label": labels,
    "text" : texts
})

out = open('ex2_res.txt','w')
out.write(df.to_string())
out.close()
