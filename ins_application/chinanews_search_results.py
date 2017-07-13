#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

def get_links(web_data, fname, query, parser='html.parser'):
    soup = BeautifulSoup(web_data, parser)
    tables = soup.find("div", {"id": "news_list"}).find_all('table', cellpadding ="0", cellspacing ="0")
    items = []
    fw = open(fname, "a")
    hrefs = []
    for table in tables:
        title_a = table.find("li", {"class": "news_title"}).find("a")
        title = title_a.text.replace("\n", "")
        url = title_a.get("href")
        summary = table.find("li", {"class": "news_content"}).text.replace("\n", "")
        news_other = table.find("li", {"class": "news_other"}).text.replace("\n", "")
        text = u"|text|".join([title, url, summary, news_other, query])
        items.append(text)
        fw.write(text.encode("utf-8") + "\n")
        hrefs.append(url)
    fw.close()

    return hrefs


def crawl_search_results(query, filename):
    base_url = "http://sou.chinanews.com/search.do"
    search_url = base_url + "?q=" + query

    cnt = 1
    install_folder = os.path.abspath(os.path.split(__file__)[0])
    geckodriver_path = os.path.join(install_folder, "./google/geckodriver.exe")
    driver = webdriver.Firefox(executable_path=geckodriver_path)

    driver.get(search_url)
    web_data = driver.page_source
    hrefs = get_links(web_data, filename, query.decode("utf-8"))
    while (True) :
        print 'Processing page %d' % (cnt)
        try:
            # next_page = driver.find_element_by_link_text('下一页')
            next_page = driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
        except Exception:
            time.sleep(2)
            continue
        try:
            driver.execute_script("arguments[0].click();", next_page)
            # next_page.click()
        except Exception:
            time.sleep(2)
            continue

        web_data = driver.page_source
        hrefs = get_links(web_data, filename, query.decode("utf-8"))
        if cnt % 5 == 0:
            time.sleep(2)
        cnt += 1

if __name__ == '__main__':
    querys = ['国家发展和改革委员会', '国家发改委', '发改委']
    filename = "fagaiwei_search_results1.txt"
    for query in querys:
        crawl_search_results(query, filename)
