#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

def get_links(web_data, parser='html.parser'):
    hrefs = []
    soup = BeautifulSoup(web_data, parser)
    lis = soup.find_all('li', 'news_title')
    for li in lis:
        for a in li.find_all('a', href=True):
            hrefs.append(a['href'])
    return hrefs


def crawl_search_results(query):
    base_url = "http://sou.chinanews.com/search.do"
    search_url = base_url + "?q=" + query

    hrefs = list()
    cnt = 1
    driver = webdriver.Firefox()
    driver.get(search_url)
    web_data = driver.page_source
    hrefs.extend(get_links(web_data))
    while (True) :
        print 'Processing page %d' % (cnt)
        next_page = driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
        """
        try:
            # next_page = driver.find_element_by_link_text('下一页')
            next_page = driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
        except Exception:
            break
        """
        driver.execute_script("arguments[0].click();", next_page)
        """
        try:
            driver.execute_script("arguments[0].click();", next_page)
            # next_page.click()
        except Exception:
            break
        """

        web_data = driver.page_source
        hrefs.extend(get_links(web_data))
        if cnt % 5 == 0:
            time.sleep(2)
        cnt += 1

    return hrefs

if __name__ == '__main__':
    query = '国家发展和改革委员会'
    hrefs = crawl_search_results(query)
    ofile = open("links2crawl_" + "1" + ".txt", 'w')
    for h in hrefs:
        ofile.write(h+'\n')
    ofile.close()


