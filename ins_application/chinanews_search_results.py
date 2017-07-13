#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import urllib  
import urllib2 

def get_links(web_data, fname, query, parser='html.parser'):
    soup = BeautifulSoup(web_data, parser)
    try:
        tables = soup.find("div", {"id": "news_list"}).find_all('table', cellpadding ="0", cellspacing ="0")
    except:
        return "error"
    items = []
    fw = open(fname, "a")
    hrefs = []
    for table in tables:
        title_a = table.find("li", {"class": "news_title"}).find("a")
        title = title_a.text.replace("\n", "").replace("\r", "")
        url = title_a.get("href").replace("\n", "").replace("\r", "")
        summary = table.find("li", {"class": "news_content"}).text.replace("\n", "").replace("\r", "")
        try:
            news_other = table.find("li", {"class": "news_other"}).text.replace("\n", "").replace("\r", "")
        except:
            news_other = ""
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
            time.sleep(1)
            continue
        try:
            driver.execute_script("arguments[0].click();", next_page)
            # next_page.click()
        except Exception:
            time.sleep(1)
            continue

        try:
            web_data = driver.page_source
        except:
            time.sleep(1)
            continue
        hrefs = get_links(web_data, filename, query.decode("utf-8"))
        if hrefs == "error":
            time.sleep(1)
            continue
        if cnt % 5 == 0:
            time.sleep(2)
        cnt += 1

def crawl_search_post(query, filename, count):
    base_url = "http://sou.chinanews.com/search.do"
    per_page = 100
    start = 0
    while start < count:
        data = {
            "field": "content", 
            "q": query,
            "ps": str(per_page),
            "start": str(start),
            "adv": "1",
            "time_scope": "0",
            "day1": "2003-01-01",
            "day2": "2017-07-13",
            "channel": "all",
            "creator": "",
            "sort": "pubtime"
        }
        result = post(base_url, data)
        hrefs = get_links(result, filename, query.decode("utf-8"))
        if hrefs != "error":
            if len(hrefs) == 0:
                start += 1
            start += len(hrefs)
            print "count %s:" % start, len(hrefs)
        else:
            pass
        time.sleep(1)
 
  
def post(url, data):  
    req = urllib2.Request(url)  
    data = urllib.urlencode(data)  
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data)  
    return response.read() 


if __name__ == '__main__':
    querys = ['国家发展和改革委员会', '国家发改委'] # ['发改委']
    filename = "fagaiwei_search_results2.txt"
    count = 90255
    for query in querys:
        crawl_search_post(query, filename, count)
        #crawl_search_results(query, filename)
