#-*-coding: utf-8-*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

from goose import Goose
from goose.text import StopWordsChinese
from hanziconv import HanziConv
import sys
from zhopenie.extractor import Extractor

def main(argv):

    url  = 'https://www.dbs.com/hongkong-zh/about-us/our-management/piyush-gupta/default.page'
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    # g.extract(raw_html=raw_html)
    data = HanziConv.toSimplified(u''.join(article.cleaned_text[:])).encode('utf-8')
    data = data.replace('\n', ' ').replace('\r', '')
    print(data)	
	
    extractor = Extractor()
    extractor.load()
    extractor.chunk_str(data)
    extractor.resolve_all_conference()
    print("Triple: ")
    print('\n'.join(str(p) for p in extractor.triple_list))
	
    extractor.release()


if __name__ == "__main__":
	main(sys.argv)
