from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep

opts = Options()
opts.add_argument('-headless')

browser = Firefox(options=opts)
browser.get('https://duckduckgo.com')

search_form = browser.find_element_by_id('search_form_input_homepage')
search_form.send_keys('real python')
search_form.submit()

sleep(10)

results = browser.find_elements_by_class_name('result')
print(results[0].text)

print(results[0])

browser.save_screenshot('/home/fanelesibonge/Documents/tes2.png')
browser.quit()
