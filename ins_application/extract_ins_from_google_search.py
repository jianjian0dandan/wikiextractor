#-*-coding: utf-8-*-

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ins_posfix = []
with open("ins_dict.txt") as f:
    for line in f:
        ins_posfix.append(line.strip().decode("utf-8"))


def is_nt(text):
    """text: unicode
    """
    def check(text):
        isins = False
        for i in range(0, 4):
            length = 4 - i
            if text[-length:] in ins_posfix and u":" not in text:
                isins = True
                break
        return isins

    isins = check(text)
    
    if not isins:
        isins = check(text.split(u"（")[0])

    return isins

def contains_nt_posfix(text):
    """text: unicode
    """
    can = "" 
    iscontain = False
    for posfix in ins_posfix:
        if posfix in text:
            iscontain = True
            prefix = text.split(posfix)[0]
            can = prefix + posfix
            if len(can) > 20:
                return False, can
            #print text, "------", text.split(posfix)[0], "-----", posfix, "------", can
            break

    return iscontain, can

def get_zh_word(str_):
    """str_: unicode
    """
    zh_word = u''
    for ch in str_:
        if u'\u4e00' <= ch <= u'\u9fff':
            zh_word += ch
        elif ch in [u'.', u',', u'、', u'。', u'，']:
            zh_word += ch
        elif ch in [str(i).decode("utf-8") for i in range(0, 10)]:
            zh_word += ch
    return zh_word

def remove_num_word(str_):
    """str_: unicode
    """
    zh_word = u''
    for ch in str_:
        if not ch in [str(i).decode("utf-8") for i in range(0, 10)]:
            zh_word += ch
    return zh_word

def parse_line(line):
    data = line.strip().replace("\n", "").split("|text|")
    summary = data[2].decode("utf-8").replace(u"网页快照", u"")
    summary = get_zh_word(summary)

    pattern = data[4].replace(u"\"", u"").decode("utf-8")            
    pattern_ = pattern.replace(u"*", u"([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)")

    return summary, pattern, pattern_

def first_filter(summary, pattern, pattern_):
    results = []
    RE = re.compile(pn_)
    candidates = RE.findall(summary)
    for candidate in candidates:
        iscontain_, can_ = contains_nt_posfix(candidate)
        if iscontain_:
            result = pn.replace(u"*", can_).strip()
            isresult = u"是" + result
            if result == u"" or u"哪些" in result or u"是不是" in result:
                continue
            
            pn1_ = u"([0-9a-zA-Z-_⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+)" + isresult
            RE1 = re.compile(pn1_)
            if len(RE1.findall(summary)):
                candidates1 = RE1.findall(summary)
                candidate = candidates1[0]
            elif len(RE1.findall(summary.replace(u"，", ""))):
                candidates2 = RE1.findall(summary.replace(u"，", ""))
                candidate = candidates2[0]
            elif len(RE1.findall(summary.replace(u",", ""))):
                candidates3 = RE1.findall(summary.replace(u",", ""))
                candidate = candidates3[0]
            else:
                candidate = result
            if not candidate.endswith(u"不") and not candidate.endswith(u"非") and u"谎称" not in candidate and len(candidate) > 1:
                if candidate.endswith(u"司司") or candidate.endswith(u"处处"):
                    candidate = candidate[:len(candidate) - 1]
                if u"年" in candidate or u"月" in candidate or u"日" in candidate:
                    candidate = candidate.replace(u"年", u"").replace(u"月", u"").replace(u"日", u"")
                candidate = remove_num_word(candidate)
                candidate = candidate.replace(u"成立于", u"").replace(u"发改委下属", u"").replace(u"国家发改委下属", u"").replace(u"国家发展和改革委员会下属", u"").replace(u"发改委所属", u"").replace(u"国家发改委所属", u"").replace(u"国家发展和改革委员会所属", u"").replace(u"发改委直属", u"").replace(u"国家发改委直属", u"").replace(u"国家发展和改革委员会直属", u"")
                candidate = candidate.replace(u"的", u"")
                if candidate == u"":
                	continue
                results.append(candidate)

    return results


if __name__ == '__main__':
    ins_set = set()
    with open("jiagesi_search_results.txt") as f:
        for line in f:
            summary, pn, pn_ = parse_line(line)
            
            results = first_filter(summary, pn, pn_)
            for r in results:
                if r not in ins_set:
                    #print '=========='
                    ins_set.add(r)
                    print r#, "-----------", summary
