#-*-coding: utf-8-*-

import json

def is_title_bz2(text):
    if text.startsWith("[[") and  text.endsWith("]]"):
        return True
    else:
        return False


if __name__=="__main__":
    keys = [u'name', u'url', u'content', u'first_in', u'last_modify', u'html', u'_id']
    # name: 四天工作制 
    # url: https://wikipedia.kfd.me/wiki/%E5%9B%9B%E5%A4%A9%E5%B7%A5%E4%BD%9C%E5%88%B6
    f = open("citiao_20170317.json")
    for line in f:
        item = json.loads(line.strip())
        print item.keys()
        print type(item["name"]), item["url"]
        print item["html"]
        print item["content"]
        break
    f.close()

