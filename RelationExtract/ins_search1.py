#-*-coding: utf-8-*-
"""用代理的话，需要从https://www.us-proxy.org/找支持https的匿名代理服务器放在proxy_urls.txt中
   使用selenium需要pip install selenium，安装最新版本的firefox浏览器，下载https://github.com/mozilla/geckodriver/releases, 放到google文件夹下
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from google import search

import time
import random
import json

if __name__ == '__main__':
    query = []
    with open("sample_50.json") as f:
        datastr = f.readline().strip()
        data = json.loads(datastr)
        for d in data:
            d = [_.encode("utf-8") for _ in d]
            origin_q = "|.|".join(d)
            entity1 = d[0].replace("<", "").replace(">", "").split("_")
            entity1 = " ".join(entity1)
            entity2 = d[2].replace("<", "").replace(">", "").split("_")
            entity2 = " ".join(entity2)
            query.append([entity1 + " " + entity2, origin_q])

    fw = open("sample_50_results.json", "w")
    crawl = False
    for idx, q in enumerate(query):
        print idx, "-----------------------------"
        q1, q2 = q
        if idx == 5:
            crawl = True
        if not crawl:
            continue
        result = search(q1, tld='com', lang='en', stop=100)

        for r in result:
            url, title, summary, ems = r
            #print title
            fw.write("%s|text|%s|text|%s|text|%s|text|%s\n" % (url, title.encode("utf-8"), summary.encode("utf-8"), ems.encode("utf-8"), q2))
        time.sleep(random.randint(5, 15))
    fw.close()
