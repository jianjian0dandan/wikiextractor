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