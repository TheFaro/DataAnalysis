import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
print('\n')

print(soup.find_all('p', class_='outer-text'))
print('\n')
print(soup.find_all(id='first'))
print('\n')
print(soup.select('div p'))