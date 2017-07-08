# -*-coding:utf-8-*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from mapping import es

SIZE_COUNT = 10000

def query_body_1():
    INDEX_NAME = "db"
    DOC_TYPE = "zhinfo"
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term": {"source": "wiki"}}, # 消息来源是wiki
                    {"wildcard":{"content": "*成立于*"}}
                ]
            }
        },
        "size": SIZE_COUNT, # 最多返回
        "sort": {}# {"timestamp":{"order": "desc"}} # asc，按照时间先后顺序返回
    }

    ff = open("test1.txt","w")
    results = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_body)["hits"]["hits"]
    for item in results:
        ff.write("%s\n" % item["_source"]["content"])

    print "finish"

    ff.close()


def query_body_2():
    INDEX_NAME = "db"
    DOC_TYPE = "zhinfo"
    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"term": {"source": "wiki"}}, # 消息来源是wiki
                    {"term": {"content_analyzedzh": "成立"}}
                ]
            }
        },
        "size": SIZE_COUNT, # 最多返回
        "sort": {}# {"timestamp":{"order": "desc"}} # asc，按照时间先后顺序返回
    }

    ff = open("test2.txt","w")
    results = es.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query_body)["hits"]["hits"]
    for item in results:
        ff.write("%s\n" % item["_source"]["content"])

    print "finish"

    ff.close()


if __name__ == "__main__":
    query_body_1()
    query_body_2()

