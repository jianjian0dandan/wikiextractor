#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2

def getFormData(q, ps, start):
	form_data = {
        "q": q,
        "ps": ps,
        "start": start,
        "sort": "pubtime",
        "time_scope": 0,
        "channel": "all",
        "adv": 1
    }
    formData = urllib.urlencode(form_data)  
    return formData 


url = "http://sou.chinanews.com/search.do?q=%E5%8F%91%E6%94%B9%E5%A7%94"
formData = getFormData("发改委", 10, 60)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}  
req = urllib2.Request(  
    url = url,  
    data = formData,  
    headers = headers  
)  
result = urllib2.urlopen(req)  
text = result.read()
print text
