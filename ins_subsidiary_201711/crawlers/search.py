#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import uniform as r
from time import sleep

from parse_search import parse

# Заголовки
username = 'linhao.lh@qq.com'
password = 'xuanxue246'

geckodriver_path = os.path.join("./", "geckodriver.exe")
browser = webdriver.Firefox(executable_path=geckodriver_path)

# Открываем главную
main = browser.get('https://www.linkedin.com')

# Получаем нужные элементы и выполняем соответствующие действия для них:
browser.find_element_by_css_selector("input[name=session_key]").send_keys(username)
browser.find_element_by_css_selector("input[name=session_password]").send_keys(password)
browser.find_element_by_id("login-submit").click()


search = browser.get('https://www.linkedin.com/search/results/companies/?keywords=Ministry%20of%20the%20Armed%20Forces(France)&origin=SWITCH_SEARCH_VERTICAL')

page_content = browser.page_source
with open("linkedin_search.txt", "w") as fw:
	fw.write("%s\n" % page_content)

"""
while 1:

    link_list = browser.find_elements_by_partial_link_text('Connect')
    for link in link_list:
        link.click()
        sleep(r(0.2, 5.2))
    browser.find_element_by_partial_link_text('Next').click()
    cur = browser.current_url
    print(cur)
    browser.get(cur)
"""

# browser.find_element_by_partial_link_text('Next').click()
# print(browser.find_element_by_css_selector("input[name='firstName.string']").get_attribute('value'))
# print(browser.find_element_by_css_selector("input[name='lastName.string']").get_attribute('value'))