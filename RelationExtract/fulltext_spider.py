#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
from selenium import webdriver
import urllib2
#from extractHtmlContent import htmlContentExtract

if __name__ == '__main__':
    url2time_dict = dict()
    fulltext_filename = "dbpedia_1113_results_fulltext.txt"
    crawled_urls = set()
    if os.path.exists(fulltext_filename):
        with open(fulltext_filename) as f:
            for line in f:
                data = line.strip().split("|text|")
                crawled_urls.add(data[0])

    urls = set()
    with open("dbpedia_1113_results_final.txt") as f:
        for line in f:
            data = line.strip().split("|text|")
            urls.add(data[0])

    print len(urls), len(crawled_urls)
    task = urls - crawled_urls
    print len(task)
    
    #install_folder = os.path.abspath(os.path.split(__file__)[0])
    #geckodriver_path = os.path.join(install_folder, "./google/geckodriver.exe")
    #driver = webdriver.Firefox(executable_path=geckodriver_path)

    def geturl(url):
        ct = 0
        RETRY_TIMES = 2
        while (True) :
            print 'Processing page %s' % (url)
            try:
                #driver.get(url)
                #web_data = driver.page_source
                web_data = urllib2.urlopen(url, timeout=5).read()#.decode("gb2312")
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
        content = geturl(url)
        if content is not None:
            content = content.replace("\n", "").replace("\r", "")
            fw.write("%s|text|%s\n" % (url, content))
        #if cnt % 10 == 0:
        #    time.sleep(2)
        cnt += 1
    fw.close()