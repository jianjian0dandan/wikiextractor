#-*-coding: utf-8-*-

import jieba
import jieba.posseg as pseg
from recognize_with_jieba import is_nt

import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

jieba.load_userdict("self_dict.txt")

add_ins_titles = set()
with open("ins_titles_zhwiki.txt") as f:
    for line in f:
        ins_title = line.strip()
        result = is_nt(ins_title)
        if result[1] or (not result[0] and not result[1]):
            add_ins_titles.add(ins_title)

with open("self_dict.txt") as f:
    for line in f:
        data = line.strip().split(" ")
        if data[2] == "nt":
            add_ins_titles.add(data[0])

fw = open("self_dict.txt", "w")
for t in add_ins_titles:
    fw.write("%s %s %s\n" % (t, "3", "nt"))
fw.close()
