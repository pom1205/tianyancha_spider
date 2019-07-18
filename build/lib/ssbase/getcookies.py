from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import time

list = ['北京邦信阳知识产权服务有限公司']

for i in list:
    url = 'https://www.tianyancha.com/search?key={}'.format(i)
    browser = webdriver.Firefox()
    wait = WebDriverWait(browser,10)
    browser.get(url)
    browser.delete_all_cookies()
    time.sleep(30)
    cookie = browser.get_cookies()
    print(cookie)