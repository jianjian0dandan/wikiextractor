#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from BeautifulSoup import BeautifulSoup

import os
import time
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

folder = os.path.join("./", "./data/")

def parse_company_profile(data):
	soup = BeautifulSoup(data)
	about = soup.find("div", {"id": "org-about-company-module"})
	about_desciption = about.text
	print soup
	afful = soup.find("div", {"class": "org-related-companies-module__related-companies-lists"})
	afflist = afful.findAll("li", {"class": "org-related-companies-module__item-row org-related-companies-module__item-row--two pt0 pr4 pb4 org-related-companies-module__item-row--is-collapsed"})
	
	for aff in afflist:
		cdiv = aff.find("div", {"class": "company-name-link ember-view"})
		print cdiv.get("href"), cdiv.text

f = open("company_list.txt")
for line in f:
	url, name = line.strip().split(",")
	browser.get(url)
	data = browser.page_source
	time.sleep(1)
	parse_company_profile(data)
	break
f.close()
