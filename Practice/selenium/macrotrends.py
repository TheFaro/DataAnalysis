from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup

opts = Options()
opts.add_argument('-headless')

browser = Firefox(options=opts)
browser.get('https://www.macrotrends.net/stocks/stock-screener')

sleep(10)
browser.save_screenshot('/home/fanelesibonge/Documents/first.png')

#parse with beautiful soup
soup = BeautifulSoup(browser.page_source, 'lxml')
table = soup.find(id='contentjqxGrid')

print(table)

'''
next_path = '/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[10]/div/div[4]/div'
next_button = browser.find_element_by_xpath(next_path).click()

sleep(10)
browser.save_screenshot('/home/fanelesibonge/Documents/second.png')
'''
browser.quit()