import requests
from bs4 import BeautifulSoup

page = requests.get("https://finance.yahoo.com/quote/UUP/history?p=UUP")
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.table
tbody = soup.tbody

print(tbody)