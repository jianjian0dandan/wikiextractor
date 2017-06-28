#-*-coding: utf-8-*-

import nltk
from collections import Counter

import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

def extract_ne_en(text):
    """text: utf-8
       refer to: http://www.nltk.org/book/ch07.html#ex-ie4
                 http://www.cnblogs.com/webRobot/p/6080155.html
       import nltk
       nltk.download() # punkt averaged_perceptron_tagger maxent_ne_chunker
       tokenizers/punkt/english.pickle
       taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle
       chunkers/maxent_ne_chunker/english_ace_binary.pickle
       corpora/words
    """
    if isinstance(text, str):
        text = text.decode("utf-8")
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    entity_names = []
    for tree in chunked_sentences:
        entity_names.extend(extract_entity_names(tree))

    entity_names = list(set(entity_names))
    result = map_entity2sent(text, entity_names)

    return result


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def map_entity2sent(text, entities):
    en_dict = dict()
    sentences = nltk.sent_tokenize(text)
    for sent in sentences:
        for entity in entities:
            if entity in sent:
                try:
                    en_dict[entity].append(sent)
                except KeyError:
                    en_dict[entity] = [sent]

    return en_dict


if __name__ == '__main__':
    texts = 'For other uses, see ISIL (disambiguation), ISIS (disambiguation), Daish (disambiguation), and Islamic state (disambiguation).Islamic State of Iraq and the Levantالدولة الإسلامية في العراق والشام‎ad-Dawlah al-Islāmiyah fī \'l-ʿIrāq wa-sh-ShāmParticipant in the Iraq War (2003–2011), Iraqi insurgency, Syrian Civil War, Iraqi Civil War, Second Libyan Civil War, Boko Haram insurgency, War in North-West Pakistan, War in Afghanistan, Yemeni Civil War, and other conflictsPrimary target of Operation Inherent Resolve and of the military intervention against ISIL: in Syria, Iraq, Libya, and Nigeria.ISIL originated as Jama\'at al-Tawhid wal-Jihad in 1999, which pledged allegiance to al-Qaeda and participated in the Iraqi insurgency following the 2003 invasion of Iraq by Western forces. The group proclaimed itself a worldwide caliphate[52][53] and began referring to itself as Islamic State (الدولة الإسلامية ad-Dawlah al-Islāmiyah) or IS[54] in June 2014. As a caliphate, it claims religious, political, and military authority over all Muslims worldwide.[55] Its adoption of the name Islamic State and its idea of a caliphate have been widely criticised, with the United Nations, various governments, and mainstream Muslim groups rejecting its statehood.[56]In Syria, the group conducted ground attacks on both government forces and opposition factions, and by December 2015 it held a large area in western Iraq and eastern Syria containing an estimated 2.8 to 8 million people,[57][58] where it enforced its interpretation of sharia law. ISIL is now believed to be operational in 18 countries across the world, including Afghanistan and Pakistan, with "aspiring branches" in Mali, Egypt, Somalia, Bangladesh, Indonesia, and the Philippines.[59][60][61][62] As of 2015, ISIL was estimated to have an annual budget of more than US$1 billion and a force of more than 30,000 fighters.[63]'
    print "-----------\n"
    result = extract_ne_en(texts)
    for k, v in result.iteritems():
        print "实体名称: ", k
        print "下面是实体出现的句子: "
        for idx, sent in enumerate(v):
            print "句子%s: " % idx, sent