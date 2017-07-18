#-*-coding: utf-8-*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import json
from mapping import es
from extractHtmlContent import htmlContentExtract

def split_fix_size(str_, lan):
    """ str_: utf-8
    """
    if lan == "zh":
        fix_size = 32800 / 4
        splitlabel = u"。"
    elif lan == "en":
        fix_size = 32700
        splitlabel = u"."

    if not isinstance(str_, unicode):
        str_ = str_.decode("utf-8")

    results_str_list = []
    while 1:
        if len(str_) > fix_size:
            temp_str = str_[:fix_size]
            lastindexofsplit = temp_str.rfind(splitlabel)
            if lastindexofsplit != -1 and lastindexofsplit != 0:
                results_str_list.append(str_[:lastindexofsplit])
                str_ = str_[lastindexofsplit+1:]
            else:
                results_str_list.append(temp_str)
                str_ = str_[fix_size:]
        else:
            results_str_list.append(str_)
            break

    return [s.encode("utf-8") for s in results_str_list]


def index_data(folder="20170612data/zh/wiki", source="wiki", lan="zh"):
    bulk_action = []
    index_count = 0
    indexname = "db"
    fnames = os.listdir(folder)

    if lan == "zh":
        doctype = "zhinfo"
        for fname in fnames:
            print fname
    elif lan == "en":
        doctype = "eninfo"

    """
    for fname in fnames:
        filename = os.path.join(folder, fname)
        data = ""
        with open(filename) as f:
            data = f.read()

        # 建索引的代码从这里开始写
        sents = split_fix_size(data, lan)

        for idx, sent in enumerate(sents):
            index_dict = dict()
            index_dict["source"] = source
            index_dict["content"] = sent
            if lan == "zh":
                index_dict["content_analyzedzh"] = sent
            elif lan == "en":
                index_dict["content_analyzeden"] = sent
            index_dict["path"] = filename + "_seg" + str(idx)
            bulk_action.extend([{"index":{"_id": filename + "_seg" + str(idx)}}, index_dict])
            index_count += 1

            if index_count !=0 and index_count % 100 == 0:
                es.bulk(bulk_action, index=indexname, doc_type=doctype)
                bulk_action = []
                print "finish index: ", index_count, source, lan

    if len(bulk_action):
        es.bulk(bulk_action, index=indexname, doc_type=doctype)
        index_count += len(bulk_action) / 2
        bulk_action = []
        print "finish index: ", index_count, source, lan
    """

def index_json(filename="", source="wiki", lan="zh"):
    bulk_action = []
    index_count = 0
    indexname = "db"

    if lan == "zh":
        doctype = "zhinfo"
    elif lan == "en":
        doctype = "eninfo"

    #g = Goose({'stopwords_class': StopWordsChinese})
    if filename != "":
        data = ""
        f = open(filename)
        for line in f:
            item = json.loads(line.strip())
            raw_html = item["html"]
            url = item["url"]
            #data = g.extract(raw_html=raw_html)
            #data = HanziConv.toSimplified(u''.join(data.cleaned_text[:])).encode('utf-8')
            #data = (u''.join(data.cleaned_text[:])).encode('utf-8')
            data = htmlContentExtract(raw_html)

            # 建索引的代码从这里开始写
            sents = split_fix_size(data, lan)

            for idx, sent in enumerate(sents):
                index_dict = dict()
                index_dict["source"] = source
                index_dict["content"] = sent
                if lan == "zh":
                    index_dict["content_analyzedzh"] = sent
                elif lan == "en":
                    index_dict["content_analyzeden"] = sent
                index_dict["path"] = filename + "_seg" + str(idx)
                bulk_action.extend([{"index":{"_id": url + "_seg" + str(idx)}}, index_dict])
                index_count += 1

                if index_count !=0 and index_count % 100 == 0:
                    es.bulk(bulk_action, index=indexname, doc_type=doctype)
                    bulk_action = []
                    print "finish index: ", index_count, source, lan
        f.close()

    if len(bulk_action):
        es.bulk(bulk_action, index=indexname, doc_type=doctype)
        index_count += len(bulk_action) / 2
        bulk_action = []
        print "finish index: ", index_count, source, lan

def index_sents(filename="", source="wiki", lan="zh"):
    bulk_action = []
    index_count = 0
    indexname = "db2"

    if lan == "zh":
        doctype = "zhinfo"
    elif lan == "en":
        doctype = "eninfo"

    if filename != "":
        data = ""
        f = open(filename)
        for id_, line in enumerate(f):
            url = str(id_)
            data = line.strip()

            # 建索引的代码从这里开始写
            sents = split_fix_size(data, lan)

            for idx, sent in enumerate(sents):
                index_dict = dict()
                index_dict["source"] = source
                index_dict["content"] = sent
                if lan == "zh":
                    index_dict["content_analyzedzh"] = sent
                elif lan == "en":
                    index_dict["content_analyzeden"] = sent
                index_dict["path"] = filename + "_seg" + str(idx)
                bulk_action.extend([{"index":{"_id": url + "_seg" + str(idx)}}, index_dict])
                index_count += 1

                if index_count !=0 and index_count % 100 == 0:
                    es.bulk(bulk_action, index=indexname, doc_type=doctype)
                    bulk_action = []
                    print "finish index: ", index_count, source, lan
        f.close()

    if len(bulk_action):
        es.bulk(bulk_action, index=indexname, doc_type=doctype)
        index_count += len(bulk_action) / 2
        bulk_action = []
        print "finish index: ", index_count, source, lan

def index_google_news(filename="", source="google_search", lan="zh"):
    bulk_action = []
    index_count = 0
    indexname = "db1"

    if lan == "zh":
        doctype = "zhinfo"
    elif lan == "en":
        doctype = "eninfo"

    if filename != "":
        data = ""
        f = open(filename)
        for id_, line in enumerate(f):
            d = line.strip().split("|text|")
            url = d[0]
            data = d[1] + d[2]

            # 建索引的代码从这里开始写
            sents = split_fix_size(data, lan)

            for idx, sent in enumerate(sents):
                index_dict = dict()
                index_dict["source"] = source
                index_dict["content"] = sent
                if lan == "zh":
                    index_dict["content_analyzedzh"] = sent
                elif lan == "en":
                    index_dict["content_analyzeden"] = sent
                index_dict["path"] = filename + "_seg" + str(idx)
                bulk_action.extend([{"index":{"_id": url + "_seg" + str(idx)}}, index_dict])
                index_count += 1

                if index_count !=0 and index_count % 100 == 0:
                    es.bulk(bulk_action, index=indexname, doc_type=doctype)
                    bulk_action = []
                    print "finish index: ", index_count, source, lan
        f.close()

    if len(bulk_action):
        es.bulk(bulk_action, index=indexname, doc_type=doctype)
        index_count += len(bulk_action) / 2
        bulk_action = []

def index_fagaiwei_content(filename="", source="chinanews", lan="zh"):
    bulk_action = []
    index_count = 0
    indexname = "db3"

    if lan == "zh":
        doctype = "zhinfo"
    elif lan == "en":
        doctype = "eninfo"

    if filename != "":
        data = ""
        f = open(filename)
        for id_, line in enumerate(f):
            d = line.strip().split("|text|")
            url = d[0]
            data = d[1]

            # 建索引的代码从这里开始写
            sents = split_fix_size(data, lan)

            for idx, sent in enumerate(sents):
                index_dict = dict()
                index_dict["source"] = source
                index_dict["content"] = sent
                if lan == "zh":
                    index_dict["content_analyzedzh"] = sent
                elif lan == "en":
                    index_dict["content_analyzeden"] = sent
                index_dict["path"] = filename + "_seg" + str(idx)
                bulk_action.extend([{"index":{"_id": url + "_seg" + str(idx)}}, index_dict])
                index_count += 1

                if index_count !=0 and index_count % 100 == 0:
                    es.bulk(bulk_action, index=indexname, doc_type=doctype)
                    bulk_action = []
                    print "finish index: ", index_count, source, lan
        f.close()

    if len(bulk_action):
        es.bulk(bulk_action, index=indexname, doc_type=doctype)
        index_count += len(bulk_action) / 2
        bulk_action = []


if __name__ == '__main__':
    """
    index_data(folder="20170612data/zh/News", source="news", lan="zh")
    index_data(folder="20170612data/zh/dissertation/Armedorganization", source="armedorganization", lan="zh")
    index_data(folder="20170612data/zh/dissertation/CIA", source="cia", lan="zh")
    index_data(folder="20170612data/zh/dissertation/Safety", source="safety", lan="zh")
    index_data(folder="20170612data/en/News", source="news", lan="en")
    index_data(folder="20170612data/en/dissertation/Armedorganization", source="armedorganization", lan="en")
    index_data(folder="20170612data/en/dissertation/CIA", source="cia", lan="en")
    index_data(folder="20170612data/en/dissertation/Safety", source="safety", lan="en")
    index_json(filename="../citiao_20170317.json", source="wiki", lan="zh")
    """
    #index_sents(filename="../ins_application/sents.txt", source="chinanews", lan="zh")
    #index_google_news(filename="../ins_application/fagaiwei_search_results.txt", source="google_search", lan="zh")
    index_fagaiwei_content(filename="../ins_application/chinanews_fagaiwei_content.txt", source="chinanews", lan="zh")
