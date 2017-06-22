#-*-coding: utf-8-*-
"""词性对照表参考： http://www.bubuko.com/infodetail-735296.html
"""

import jieba
import jieba.posseg as pseg
from collections import Counter

jieba.load_userdict("self_dict.txt")

ins_pos_set = set(["nt"])
per_pos_set = set(["nr", "nr1", "nr2", "nrj", "nrf"])
loc_pos_set = set(["ns", "nsf"])

def extract_ne(text):
    """抽取text中的机构实体
       text: utf-8 编码
    """
    nts = [] # institutions
    nps = [] # persons
    nls = [] # locations
    words = pseg.cut(text)
    for w in words:
        flag = w.flag
        word = w.word
        if flag in ins_pos_set:
            nts.append(word)
        elif flag in per_pos_set:
            nps.append(word)
        elif flag in loc_pos_set:
            nls.append(word)

    ct = Counter(nts)
    results1 = ct.most_common()
    ct = Counter(nps)
    results2 = ct.most_common()
    ct = Counter(nls)
    results3 = ct.most_common()

    return {"ins": [r[0] for r in results1], "per": [r[0] for r in results2], \
            "loc": [r[0] for r in results3]}


def is_nt(title):
    """判断词条名称是否是机构实体，title是词条名称, 返回(是否为机构实体，是否需要将词条作为机构实体加入自定义字典)
       title: utf-8 编码
    """
    words = pseg.cut(title)
    containnt = False
    for idx, w in enumerate(words):
        flag = w.flag
        word = w.word
        # 切出一个机构实体
        if flag == "nt" and ":" not in title:
            containnt = True

    if containnt:
        if idx > 0:
            return True, True
        else:
            return True, False
    else:
        return False, False


if __name__ == '__main__':
    texts = "中华人民共和国国家发展和改革委员会，简称国家发展改革委、国家发改委，是中华人民共和国国务院的重要组成部门（以至于被称为“小国务院”），主要负责综合研究拟订经济和社会发展政策，进行总量平衡，并指导总体经济体制改革的宏观调控[1]。"
    nts = extract_nt(texts)
    print "-----------"
    for w in nts:
        print w

    texts = "伊斯兰国（阿拉伯语：الدولة الإسلامية‎，转写：ad-Dawlat al-Islamiya；英语：The Islamic State，缩写：IS），前称伊拉克和沙姆伊斯兰国（阿拉伯语：الدولة الاسلامية في العراق والشام ad-Dawlat al-Islamiyat fi al-Iraq wa-sh-Sham‎；英语：Islamic State of Iraq and al-Sham，简称ISIS）或伊拉克和黎凡特伊斯兰国（英语：Islamic State of Iraq and the Levant，简称ISIL），是一个活跃在伊拉克和叙利亚[35]的萨拉菲聖戰主義组织及其建立的未被世界广泛认可的政治實體，奉行极端保守的伊斯兰原教旨主义瓦哈比派。组织领袖巴格達迪自封为哈里发，定國號为「伊斯兰国」[1][27][36]，宣称自身对于整个穆斯林世界（包括全中东、非洲东部、中部、北部、黑海东部、南部、西部，亚洲中部和西部、欧洲伊比利半岛、印度幾乎全境、中国西部、北部地区）拥有統治地位[37][38]。周边阿拉伯国家以阿拉伯文缩写称其为「达伊沙」（阿拉伯语：داعش, Da-esh‎；da:ʕeʃ)），与阿拉伯语的“踩踏”同音，以示对其“伊斯兰国”名稱的不承认及蔑视[39][40][41]。中国媒体有时则直接以“极端组织”代指这一组织[42][43]。该组织目前致力在伊拉克及沙姆地区建立政教合一的伊斯兰国家，是叙利亚内战反政府武装中主要的圣战组织之一，并占领伊拉克北部、及敘利亞中部的部分城市和地区。其自认为是一个独立国家，声称拥有伊拉克和叙利亚的主权，而且宣稱已于2014年11月13日拥有阿拉伯地区更多的主权，涉及利比亚、埃及、阿尔及利亚、沙特阿拉伯和也门等国家。[44][45]伊斯兰国以反对偶像崇拜为理由，对占领区内的文化古迹进行摧毁。同时，伊斯兰国对俘虏及包括记者在内的平民进行斩首并拍摄视频广泛传播。这些举动使得包括联合国在内的大多数国家和组织将其定性为恐怖组织。该组织参与的戰事包括伊拉克战争及伊拉克内战（2011年－至今）、叙利亚内战、利比亞內戰（2014年－至今） 、西奈半岛动乱和阿富汗戰爭 (2015年至今)，与各阿拉伯国家政府军[46][47]（也包括叙利亚反对派[48][49]）、部分地方武装以及一些北约成员国或欧洲国家军队交战[50][51][52][53][54][55][56][57][58]。2015年12月，伊斯蘭國宣稱要攻擊以色列[59]。该组织的几个领导人曾声称时任美国总统小布什2003年发动的伊拉克戰爭是导致他们发起对美国的圣战之原因，而美军行动使他们获得士兵和最终夺回国家的控制权变得容易[60] 。伊斯兰国并不谋求参与所佔領国家的政治权力分配，其根本目的是要在中东地区建立政教合一的極端伊斯兰国。伊斯兰国实行严格的伊斯兰教法，实现「伊斯兰化」，要讓受到統治的民眾「成為真正服從的穆斯林」。而从其在伊拉克和叙利亚采取的武装行动性质可以看出该组织極權主義、军国主义、伊斯蘭法西斯主義倾向十分明显。在萨达姆·海珊被美擒獲、阿拉伯之春後卡扎菲被打倒、阿萨德等泛阿拉伯世俗主义政权式微的現今，中东面临着回到逊尼派和什叶派宗教混战的危機。事实上，目前伊拉克政府军与反政府武装力量的对抗其中一部分就是一场逊尼派和什叶派的宗教混战。海灣逊尼派宗教神權國家（有別於世俗國家）與團體（沙特阿拉伯、卡達等）對什叶派國家的敵視，與對叛亂組織或明或暗的支持和資助（该组织大部分头目来自沙烏地阿拉伯），也是造成今日混亂局面的因素之一[61]。"
    nts = extract_nt(texts)
    print "-----------"
    for w in nts:
        print w
