#-*-coding: utf-8-*-
"""用代理的话，需要从https://www.us-proxy.org/找支持https的匿名代理服务器放在proxy_urls.txt中
   使用selenium需要pip install selenium，安装最新版本的firefox浏览器，下载https://github.com/mozilla/geckodriver/releases, 放到google文件夹下
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from google import search

if __name__ == '__main__':
    query = []
    with open("ins_pattern3.txt") as f:
        for line in f:
            query.append(line.strip())

    fw = open("jingjiyunxingtiaojieju_search_results.txt", "w")
    for idx, q in enumerate(query):
        result = search(q, tld='com.hk', lang='zh', stop=None)
        for r in result:
            url, title, summary, ems = r
            print title
            fw.write("%s|text|%s|text|%s|text|%s|text|%s\n" % (url, title.encode("utf-8"), summary.encode("utf-8"), ems.encode("utf-8"), q))
    fw.close()