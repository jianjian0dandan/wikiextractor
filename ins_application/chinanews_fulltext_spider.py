#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
from selenium import webdriver
import urllib2
from extractHtmlContent import htmlContentExtract

if __name__ == '__main__':
    url2time_dict = dict()
    fulltext_filename = "fagaiwei_search_results_fagaiwei_children_fulltext.txt"
    crawled_urls = set()
    if os.path.exists(fulltext_filename):
        with open(fulltext_filename) as f:
            for line in f:
                data = line.strip().split("|text|")
                crawled_urls.add(data[0])

    urls = set()
    with open("fagaiwei_search_results_fagaiwei_children.txt") as f:
        for line in f:
            data = line.strip().split("|text|")
            urls.add(data[1])
            #print data[3]
            if "html" in data[3]:
                date = data[3].split("html")[1].strip().replace("\t", "").lstrip(" ")
            else:
                date = data[3].strip().replace("\t", "").replace(" ", "").lstrip(" ")
            url2time_dict[data[1]] = date

    task = urls - crawled_urls
    print len(task)
    
    install_folder = os.path.abspath(os.path.split(__file__)[0])
    geckodriver_path = os.path.join(install_folder, "./google/geckodriver.exe")
    #driver = webdriver.Firefox(executable_path=geckodriver_path)

    def geturl(driver, url):
        ct = 0
        RETRY_TIMES = 2
        while (True) :
            print 'Processing page %s' % (url)
            try:
                #driver.get(url)
                #web_data = driver.page_source
                web_data = urllib2.urlopen(url, timeout=5).read().decode("gb2312")
                # content = htmlContentExtract(web_data)
                content = web_data
                return content
            except:
                #time.sleep(2)
                ct += 1
                if ct > RETRY_TIMES:
                    print "Error: ", url
                    return None
                else:
                    print 'Retry...'
    
    fw = open(fulltext_filename, "a")
    cnt = 1
    for url in task:
        if not url.startswith("http://"):
            continue
        driver = ""
        content = geturl(driver, url)
        if content is not None:
            content = content.replace("\n", "")
            date = url2time_dict[url]
            fw.write("%s|text|%s|text|%s\n" % (url, content, date))
        #if cnt % 10 == 0:
        #    time.sleep(2)
        cnt += 1
    fw.close()
