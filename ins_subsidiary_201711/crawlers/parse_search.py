#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from BeautifulSoup import BeautifulSoup


def parse(data):
    soup = BeautifulSoup(data)
    results = soup.findAll("li", {"class": "search-result search-result__occluded-item ember-view"})
    lis = []
    for r in results:
        result_div = r.find("div", {"class": "search-result__info pt3 pb4 pr0"})
        a = result_div.find("a")
        h3 = result_div.find("h3")
        url = "http://www.linkedin.com" + a.get("href")
        name = h3.text
        lis.append([url, name])

    return lis

if __name__ == '__main__':
    f = open("linkedin_search.txt")
    data = f.read()
    f.close()
    data = parse(data)
    fw = open("company_list.txt", "w")
    for url, name in data:
    	fw.write("%s,%s\n" % (url, name))
    fw.close()
