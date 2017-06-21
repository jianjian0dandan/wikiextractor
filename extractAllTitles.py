#-*-coding: utf-8-*-

import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

import fileinput
from WikiExtractorV2 import pages_from
from recognize_with_jieba import extract_nt, is_nt


if __name__ == '__main__':
    input_file = "zhwiki-latest-pages-articles.xml.bz2"

    fw = open("citiao_nt_zhwiki.txt", "w")
    fwdict = open("self_dict_update.txt", "w")

    file = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)
    count = 0
    for page_data in pages_from(file):
        id, revid, title, ns, page = page_data
        # nts = extract_nt(title)

        ifnt, ifadd = is_nt(title)
        if ifnt:
            if ifadd:
                print title, ifadd
                fwdict.write("%s %s %s\n" % (title.encode("utf-8"), 3, "nt"))
                fw.write("%s\t%s\t%s\t%s\n" % (id, revid, title.encode("utf-8"), ns))
            else:
                print title, ifadd
                fw.write("%s\t%s\t%s\t%s\n" % (id, revid, title.encode("utf-8"), ns))

    fw.close()
    fwdict.close()

    self_dict = set()
    with open("self_dict.txt") as f:
        for line in f:
            self_dict.add(line.strip().split(" ")[0])

    f = open("self_dict_update.txt")
    for line in f:
        if "template" in line or "Template:" in line or "Category:" in line or "Wikipedia:" in line:
            continue

        self_dict.add(line.strip().split(" ")[0])
    f.close()

    fw = open("self_dict.txt", "w")
    for d in self_dict:
        if ":" in d:
            print d
        else:
            fw.write("%s %s %s\n" % (d, "3", "nt"))
    fw.close()

    fw = open("citiao_nt_zhwiki_final.txt", "w")
    with open("citiao_nt_zhwiki.txt") as f:
        for line in f:
            data = line.strip().split("\t")
            if ":" in data[2]:
                print data[2]
            else:
                fw.write(line)
    fw.close()
