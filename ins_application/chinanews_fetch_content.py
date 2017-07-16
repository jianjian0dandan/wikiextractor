#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def fetch_content_from_html(html):
    content = str()
    soup = BeautifulSoup(html, 'html.parser')
    paras = soup.find_all('p')
    for p in paras:
        if len(p.find_all('a')) != 0 or len(p.find_all('script')) != 0 or len(p.find_all('div')) != 0:
            continue
        text = p.getText()
        if check_contain_chinese(text):
            content += text + "\t"
    return content

def fetch_content(url2html, resultfname):
    fw = open(resultfname, "w")
    with open(url2html, 'r') as infile:
        for line in infile:
            parts = line.split('|text|')
            url = parts[0]
            html = parts[1]
            content = fetch_content_from_html(html)
            fw.write("%s|text|%s\n" % (url, content))
    fw.close()

if __name__ == '__main__':
    fetch_content('fagaiwei_search_results2_fulltext.txt', 'chinanews_fagaiwei_content.txt')
