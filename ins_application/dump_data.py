#-*-coding: utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

mongo = pymongo.MongoClient(host="219.224.134.213")
collection = mongo.client['neteasenews']['news']

fw = open("dump_neteasenews.txt", "w")
keys = [u'title', u'childclass', u'content', u'url', u'time', u'date', u'_id', u'class']
result = collection.find()
for r in result:
	data = []
	for key in keys:
		value = r[key]
		if isinstance(value, unicode):
			value = value.encode("utf-8")
		else:
			value = str(value)
		value = value.replace("\n", "")
		data.append(value)
	fw.write("|text|".join(data) + "\n")
fw.close()

