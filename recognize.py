# -*- coding: utf8 -*-
"""判断人、组织、地点
"""
import sys 
reload(sys)
sys.setdefaultencoding('utf-8') 

import os
import json
from pyltp import NamedEntityRecognizer, Segmentor, Postagger

LTP_DATA_DIR = './ltp_data'  # ltp模型目录的路径
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`ner.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`


def extract_institute(text):
    words = customized_segmentor.segment(text) # 分词
    print '\t'.join(words)
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    return "\t".join(netags)


if __name__ == '__main__':
    customized_segmentor = Segmentor()  # 初始化实例
    customized_segmentor.load(cws_model_path)  # 加载模型
    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型

    print '伊斯兰国', extract_institute('伊斯兰国')
    print '发改委', extract_institute('发改委')
    print '中华人民共和国国家发展和改革委员会', extract_institute('中华人民共和国国家发展和改革委员会')

    """
    f = open("zhwiki.json")
    for line in f:
        item = json.loads(line.strip())
        text = item["text"]
        print text
        #print extract_institute(text)
    f.close()
    """
    customized_segmentor.release() # 释放模型
    postagger.release()  # 释放模型
    recognizer.release()  # 释放模型

