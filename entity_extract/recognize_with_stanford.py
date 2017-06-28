# coding=utf-8 

''' 
    安装nltk :
    $ pip install nltk`
    添加环境变量:
    $ export CLASSPATH=".../stanford-ner.jar:$CLASSPATH"
'''

import os
import nltk
from nltk.tag import StanfordNERTagger
from collections import Counter

AB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')

def Is64Windows():
    return 'PROGRAMFILES(X86)' in os.environ

is64bit = Is64Windows()
if is64bit:
    java_path = "C:\\Program Files\\Java\\jdk1.8.0_131\\bin\\java.exe"
    os.environ['JAVAHOME'] = java_path

jar = os.path.join(AB_PATH, 'stanford-ner.jar')
st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz', jar)


def extract_entities_English(text):
    per = dict()
    loc = dict()
    org = dict()

    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        r = st.tag(sent.split())
        for w in r:
            if w[1] == 'PERSON':
                try:
                    per[w[0]].append(sent)
                except KeyError:
                    per[w[0]] = [sent]
            elif w[1] == 'LOCATION':
                try:
                    loc[w[0]].append(sent)
                except KeyError:
                    loc[w[0]] = [sent]
            elif w[1] == 'ORGANIZATION':
                try:
                    org[w[0]].append(sent)
                except KeyError:
                    org[w[0]] = [sent]

    per = sorted(per.iteritems(), key=lambda (k, v):len(v), reverse = True)
    loc = sorted(loc.iteritems(), key=lambda (k, v):len(v), reverse = True)
    org = sorted(org.iteritems(), key=lambda (k, v):len(v), reverse = True)
    entities = {
        'per': per,
        'loc': loc,
        'ins': org
    }
    return entities

if __name__ == '__main__':
    texts = 'For other uses, see ISIL (disambiguation), ISIS (disambiguation), Daish (disambiguation), and Islamic state (disambiguation).Islamic State of Iraq and the Levantالدولة الإسلامية في العراق والشام‎ad-Dawlah al-Islāmiyah fī \'l-ʿIrāq wa-sh-ShāmParticipant in the Iraq War (2003–2011), Iraqi insurgency, Syrian Civil War, Iraqi Civil War, Second Libyan Civil War, Boko Haram insurgency, War in North-West Pakistan, War in Afghanistan, Yemeni Civil War, and other conflictsPrimary target of Operation Inherent Resolve and of the military intervention against ISIL: in Syria, Iraq, Libya, and Nigeria.ISIL originated as Jama\'at al-Tawhid wal-Jihad in 1999, which pledged allegiance to al-Qaeda and participated in the Iraqi insurgency following the 2003 invasion of Iraq by Western forces. The group proclaimed itself a worldwide caliphate[52][53] and began referring to itself as Islamic State (الدولة الإسلامية ad-Dawlah al-Islāmiyah) or IS[54] in June 2014. As a caliphate, it claims religious, political, and military authority over all Muslims worldwide.[55] Its adoption of the name Islamic State and its idea of a caliphate have been widely criticised, with the United Nations, various governments, and mainstream Muslim groups rejecting its statehood.[56]In Syria, the group conducted ground attacks on both government forces and opposition factions, and by December 2015 it held a large area in western Iraq and eastern Syria containing an estimated 2.8 to 8 million people,[57][58] where it enforced its interpretation of sharia law. ISIL is now believed to be operational in 18 countries across the world, including Afghanistan and Pakistan, with "aspiring branches" in Mali, Egypt, Somalia, Bangladesh, Indonesia, and the Philippines.[59][60][61][62] As of 2015, ISIL was estimated to have an annual budget of more than US$1 billion and a force of more than 30,000 fighters.[63]'
    print "-----------\n"
    result = extract_entities_English(texts)
    print "-----------News en\n"
    print "ins:"
    for w in result["ins"]:
        print "实体名称： ", w[0]
        print "下面是实体出现的句子: "
        for idx, sent in enumerate(w[1]):
            print "句子%s: " % idx, sent
    print "\n"
    print "per:"
    for w in result["per"]:
        print "实体名称： ", w[0]
        print "下面是实体出现的句子: "
        for idx, sent in enumerate(w[1]):
            print "句子%s: " % idx, sent
    print "\n"
    print "loc:"
    for w in result["loc"]:
        print "实体名称： ", w[0]
        print "下面是实体出现的句子: "
        for idx, sent in enumerate(w[1]):
            print "句子%s: " % idx, sent

    """
    with open("./20170612data/en/News/20477.en.txt") as f:
        result = extract_entities_English(f.read())
        print "-----------News en\n"
        print "ins:"
        for w in result["ins"]:
            print w
        print "\n"
        print "per:"
        for w in result["per"]:
            print w
        print "\n"
        print "loc:"
        for w in result["loc"]:
            print w

    with open("./20170612data/en/dissertation/CIA/686.en.txt") as f:
        result = extract_entities_English(f.read())
        print "-----------CIA en\n"
        print "ins:"
        for w in result["ins"]:
            print w
        print "\n"
        print "per:"
        for w in result["per"]:
            print w
        print "\n"
        print "loc:"
        for w in result["loc"]:
            print w

    with open("./20170612data/en/dissertation/Safety/1600.en.txt") as f:
        result = extract_entities_English(f.read())
        print "-----------Safety en\n"
        print "ins:"
        for w in result["ins"]:
            print w
        print "\n"
        print "per:"
        for w in result["per"]:
            print w
        print "\n"
        print "loc:"
        for w in result["loc"]:
            print w

    with open("./20170612data/en/dissertation/Armedorganization/974.en.txt") as f:
        result = extract_entities_English(f.read())
        print "-----------Armedorganization en\n"
        print "ins:"
        for w in result["ins"]:
            print w
        print "\n"
        print "per:"
        for w in result["per"]:
            print w
        print "\n"
        print "loc:"
        for w in result["loc"]:
            print w
    """

