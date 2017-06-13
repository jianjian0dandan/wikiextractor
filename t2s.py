# -*- coding: utf8 -*-

import os
import json
# import opencc

import sys 
reload(sys)
sys.setdefaultencoding('utf-8') 

# 测试opencc繁体转简体
# cc = opencc.OpenCC('t2s')
# print cc.convert(u'Open Chinese Convert（OpenCC）「開放中文轉換」，是一個致力於中文簡繁轉換的項目，提供高質量詞庫和函數庫(libopencc)。')

if __name__ == '__main__':
    fwt = open("zhwiki.json", "w")
    folder = "./output/AA/"
    fnames = os.listdir(folder)
    keys = [u'url', u'text', u'id', u'title']
    for fname in fnames:
    	if not fname.startswith("wiki"):
    		continue
        tempname = "tmpchttext"
        tempoutputname = "tmpchstext"
        f = open(os.path.join(folder, fname))
        for line in f:
            item = json.loads(line.strip())
            with open(tempname, "w") as fw:
                fw.write("%s" % item["text"].encode("utf-8"))

            cmd = "opencc-1.0.1-win64\opencc.exe -i %s -o %s -c opencc-1.0.1-win64\\t2s.json" % (tempname, tempoutputname)
            os.popen(cmd)
            
            with open(tempoutputname) as f1:
                item["text"] = f1.read()
                fwt.write("%s\n" % json.dumps(item))
        f.close()
    fwt.close()