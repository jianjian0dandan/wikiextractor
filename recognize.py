# -*- coding: utf8 -*-
"""判断人、组织、地点
"""

import json

if __name__ == '__main__':
	f = open("zhwiki.json")
	for line in f:
		item = json.loads(line.strip())
		print item["text"]
	f.close()