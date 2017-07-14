#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
from selenium import webdriver
import urllib2

if __name__ == '__main__':
    fulltext_filename = "fagaiwei_search_results2_fulltext.txt"
    crawled_urls = set()
    if os.path.exists(fulltext_filename):
        with open(fulltext_filename) as f:
            for line in f:
                data = line.strip().split("|text|")
                crawled_urls.add(data[0])

    urls = set()
    with open("fagaiwei_search_results2.txt") as f:
        for line in f:
            data = line.strip().split("|text|")
            urls.add(data[1])

    task = urls - crawled_urls
    print len(urls), len(crawled_urls), len(task)
    
