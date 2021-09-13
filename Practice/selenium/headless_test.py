from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

browser = webdriver.Firefox(options=options)
browser.get('https://www.intellipaat.com')

browser.save_screenshot('/home/fanelesibonge/Documents/tes.png')
browser.quit()