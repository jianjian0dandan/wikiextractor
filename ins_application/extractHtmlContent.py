#-*-coding: utf-8-*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

import re
from webstemmer.htmlutils import rmsp, getencoder
from webstemmer.htmlparser3 import HTMLParser3, HTMLHandler


##  HTMLTextHandler
##
class HTMLTextHandler(HTMLHandler):

  CUTSP = re.compile(ur'([\u3000-\u9fff])\n+([\u3000-\u9fff])')
  IGNORED_TAGS = dict.fromkeys(
    'comment script style select'.split(' ')
    )
  NEWLINE_TAGS = dict.fromkeys(
    'p br div td th li blockquote pre form hr h1 h2 h3 h4 h5 h6 address'.split(' ')
    )
  
  def __init__(self, out, ignored_tags=IGNORED_TAGS, newline_tags=NEWLINE_TAGS):
    self.out = out
    self.ignored_tags = ignored_tags
    self.newline_tags = newline_tags
    self.ignore = 0
    self.text = []
    return
  
  def flush(self, newline=False):
    if self.text:
      s = rmsp(self.CUTSP.sub(r'\1\2', ''.join(self.text).strip()))
      if s:
        self.out.feed(s+'\n')
        self.text = []
    return
  
  def start_unknown(self, tag, attrs):
    if tag in self.ignored_tags:
      self.ignore += 1
    if tag in self.newline_tags:
      self.flush(True)
    return
  
  def end_unknown(self, tag):
    if tag in self.ignored_tags:
      self.ignore -= 1
    return
  
  def handle_data(self, data):
    if not self.ignore:
      self.text.append(data)
    return
  
  def finish(self):
    self.flush()
    self.out.close()
    return

class out:
    def __init__(self, charset):
        self.output = ""
        self.encoder = getencoder(charset)
        return
    def close(self): pass
    def feed(self, s):
        self.output += self.encoder(s, 'replace')[0]
        #print self.encoder(s, 'replace')[0]
        #sys.stdout.write(self.encoder(s, 'replace')[0])
        #sys.stdout.flush()
        return
    def getOutput(self):
        return self.output


def htmlContentExtract(str_):
    """str_: utf-8
    """
    (charset_in, charset_out) = ('utf-8', 'utf-8')
    ot = out(charset_out)
    p = HTMLParser3(HTMLTextHandler(ot), charset=charset_in)
    p.feed_byte(str_).close()
    return ot.getOutput()


if __name__ == "__main__":
    """
    import urllib
    url = '-'
    if url == '-':
        fp = sys.stdin
    elif url.startswith('http:') or url.startswith('ftp:'):
        fp = urllib.urlopen(url)
    else:
        fp = file(url)
    """
    (charset_in, charset_out) = ('utf-8', 'utf-8')
    url = 'test.html'
    """
    fp = file(url)
    p = HTMLParser3(HTMLTextHandler(out(charset_out)), charset=charset_in)
    p.feed_file(fp).close()
    fp.close()
    """
    with open(url) as fp:
        str_ = fp.read()
        ot = out(charset_out)
        p = HTMLParser3(HTMLTextHandler(ot), charset=charset_in)
        p.feed_byte(str_).close()
        print ot.getOutput()
