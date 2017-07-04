#-*-coding: utf-8-*-
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

process = os.popen("java -jar RecogIns.jar fagaiwei_search_results.txt %s %s 2 -1 -1" % (u"发改委,国家发改委,国家发展和改革委员会".encode("gbk"), u"司".encode("gbk")))
print process.read()
process.close()
