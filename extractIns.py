#-*-coding: utf-8-*-

import json
from BeautifulSoup import BeautifulSoup

def is_title_bz2(text):
    if text.startsWith("[[") and  text.endsWith("]]"):
        return True
    else:
        return False


if __name__=="__main__":
    ins_posfix = set()
    with open("ins_dict.txt") as f:
        for line in f:
            ins_posfix.add(line.strip().decode("utf-8"))

    keys = [u'name', u'url', u'content', u'first_in', u'last_modify', u'html', u'_id']
    # name: 四天工作制 
    # url: https://wikipedia.kfd.me/wiki/%E5%9B%9B%E5%A4%A9%E5%B7%A5%E4%BD%9C%E5%88%B6
    """
    f = open("citiao_20170317.json")
    fw = open("ins_title_json.txt", "w")
    for line in f:
        item = json.loads(line.strip())
        # print type(item["name"]), item["url"]
        title = item["name"]
        isins = False
        for i in range(0, 4):
            length = 4 - i
            if title[-length:] in ins_posfix and ":" not in title:
                isins = True
                break
        if isins:
            fw.write("%s\n" % title.encode("utf-8"))
    f.close()
    fw.close()
    """
    ins_titles = set()
    f = open("ins_title_json.txt")
    for line in f:
        ins_titles.add(line.strip().decode("utf-8"))
    f.close()

    f = open("citiao_20170317.json")
    for line in f:
        item = json.loads(line.strip())
        title = item["name"]
        if title in ins_titles:
            print item["html"]
            break
    f.close()
