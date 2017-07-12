#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from google import search
import time

def ts2datetime(ts):
    return time.strftime('%m/%d/%Y', time.localtime(ts))

def datetime2ts(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))


if __name__ == '__main__':
    keywords = ["发改委", "国家发展和改革委员会", "国家发改委"]
    tbs_list = []
    end_date = '2017-07-12'
    end_ts = datetime2ts(end_date)
    days = 365
    for i in range(0, days):
        datestr = ts2datetime(end_ts - i * 24 * 3600)
        tbs = "cdr:1,cd_min:%s,cd_max:%s" % (datestr, datestr)
        tbs_list.append(tbs)

    fw = open("keywords_fagaiwei_search_summary.txt", "w")
    for idx, q in enumerate(keywords):
        for tbs in tbs_list: 
            result = search(q, tld='com.hk', lang='zh', tbs=tbs, stop=None)
            for r in result:
                url, title, summary, ems = r
                print title
                fw.write("%s|text|%s|text|%s|text|%s|text|%s\n" % (url, title.encode("utf-8"), summary.encode("utf-8"), ems.encode("utf-8"), q))
    fw.close()
