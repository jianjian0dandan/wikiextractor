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

    tempname = "tmpchttext"
    tempoutputname = "tmpchstext"
    fw = open(tempname, "w")
    splitstr = "===================================================="
    item_list = []
    for fname in fnames:
        if not fname.startswith("wiki"):
            continue
        
        f = open(os.path.join(folder, fname))
        for line in f:
            item = json.loads(line.strip())
            item_list.append(item)
        f.close()
        """
        f = open(os.path.join(folder, fname))
        for line in f:
            item = json.loads(line.strip())
            item["text"] = cc.convert(item["text"])
            fwt.write("%s\n" % json.dumps(item))
        f.close()
        """

        """
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
        """
    for idx, item in enumerate(item_list):
        if idx > 0:
            fw.write(splitstr)
        fw.write("%s" % item["text"].encode("utf-8"))
        del item["text"]
    fw.close()

    print "start convert..."
    cmd = "opencc-1.0.1-win64\opencc.exe -i %s -o %s -c opencc-1.0.1-win64\\t2s.json" % (tempname, tempoutputname)
    os.popen(cmd)
    print "end convert..."

    texts_list = []
    with open(tempoutputname) as f:
        data = f.read()
        texts_list = data.split(splitstr)
    print "end split..."
    print len(item_list), len(texts_list)
    
    for idx, text in enumerate(texts_list):
        item = item_list[idx]
        item["text"] = text.decode("utf-8")
        fwt.write("%s\n" % json.dumps(item))

    fwt.close()