#-*-coding: utf-8-*-
"""使用之前需要pip install pynlpir以及pynlpir update
"""

import pynlpir
from pynlpir import nlpir

import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

pynlpir.open()
nh_set = ['personal name', 'Japanese personal name', 'transcribed personal name']
ns_set = ['toponym', 'transcribed toponym']
ni_set = ['organization/group name']


def get_pos(text, nh_dict, ns_dict, ni_dict, title=""):
    result = pynlpir.segment(text, pos_names='child')
    for w1,c in result:
        w = w1.encode('utf-8')
        if c in ni_set:
            if w in title:
                try:
                    ni_dict[w] = ni_dict[w] + 2
                except KeyError:
                    ni_dict[w] = 2
            else:
                try:
                    ni_dict[w] = ni_dict[w] + 1
                except KeyError:
                    ni_dict[w] = 1
            
        elif c in ns_set:
            if w in title:
                try:
                    ns_dict[w] = ns_dict[w] + 2
                except KeyError:
                    ns_dict[w] = 2
            else:
                try:
                    ns_dict[w] = ns_dict[w] + 1
                except KeyError:
                    ns_dict[w] = 1
        elif c in nh_set:
            if w in title:
                try:
                    nh_dict[w] = nh_dict[w] + 2
                except KeyError:
                    nh_dict[w] = 2
            else:
                try:
                    nh_dict[w] = nh_dict[w] + 1
                except KeyError:
                    nh_dict[w] = 1
        else:
            pass

    return nh_dict, ns_dict, ni_dict


def extract_ne(text):
    """text: utf-8
    """
    nh_dict = dict()
    ns_dict = dict()
    nt_dict = []
    ni_dict = dict()
    sents = text.split('。')
    for sent in sents:
    	try:
            nh_dict, ns_dict, ni_dict = get_pos(sent, nh_dict, ns_dict, ni_dict, title="")
        except:
        	pass
    
    nh = sorted(nh_dict.iteritems(), key=lambda d:d[1], reverse = True)
    ns = sorted(ns_dict.iteritems(), key=lambda d:d[1], reverse = True)
    ni = sorted(ni_dict.iteritems(), key=lambda d:d[1], reverse = True)

    nh = [k.strip().decode("utf-8", 'ignore') for k, v in nh]
    ni = [k.strip().decode("utf-8", 'ignore') for k, v in ni]
    ns = [k.strip().decode("utf-8", 'ignore') for k, v in ns]
    item = {
        "ins": ni,
        "per": nh,
        "loc": ns
    }

    return item


if __name__ == '__main__':
    texts = "中华人民共和国国家发展和改革委员会，简称国家发展改革委、国家发改委，是中华人民共和国国务院的重要组成部门（以至于被称为“小国务院”），主要负责综合研究拟订经济和社会发展政策，进行总量平衡，并指导总体经济体制改革的宏观调控[1]。"
    result = extract_ne(texts)
    print "-----------\n"
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

    texts = "伊斯兰国（阿拉伯语：الدولة الإسلامية‎，转写：ad-Dawlat al-Islamiya；英语：The Islamic State，缩写：IS），前称伊拉克和沙姆伊斯兰国（阿拉伯语：الدولة الاسلامية في العراق والشام ad-Dawlat al-Islamiyat fi al-Iraq wa-sh-Sham‎；英语：Islamic State of Iraq and al-Sham，简称ISIS）或伊拉克和黎凡特伊斯兰国（英语：Islamic State of Iraq and the Levant，简称ISIL），是一个活跃在伊拉克和叙利亚[35]的萨拉菲聖戰主義组织及其建立的未被世界广泛认可的政治實體，奉行极端保守的伊斯兰原教旨主义瓦哈比派。组织领袖巴格達迪自封为哈里发，定國號为「伊斯兰国」[1][27][36]，宣称自身对于整个穆斯林世界（包括全中东、非洲东部、中部、北部、黑海东部、南部、西部，亚洲中部和西部、欧洲伊比利半岛、印度幾乎全境、中国西部、北部地区）拥有統治地位[37][38]。周边阿拉伯国家以阿拉伯文缩写称其为「达伊沙」（阿拉伯语：داعش, Da-esh‎；da:ʕeʃ)），与阿拉伯语的“踩踏”同音，以示对其“伊斯兰国”名稱的不承认及蔑视[39][40][41]。中国媒体有时则直接以“极端组织”代指这一组织[42][43]。该组织目前致力在伊拉克及沙姆地区建立政教合一的伊斯兰国家，是叙利亚内战反政府武装中主要的圣战组织之一，并占领伊拉克北部、及敘利亞中部的部分城市和地区。其自认为是一个独立国家，声称拥有伊拉克和叙利亚的主权，而且宣稱已于2014年11月13日拥有阿拉伯地区更多的主权，涉及利比亚、埃及、阿尔及利亚、沙特阿拉伯和也门等国家。[44][45]伊斯兰国以反对偶像崇拜为理由，对占领区内的文化古迹进行摧毁。同时，伊斯兰国对俘虏及包括记者在内的平民进行斩首并拍摄视频广泛传播。这些举动使得包括联合国在内的大多数国家和组织将其定性为恐怖组织。该组织参与的戰事包括伊拉克战争及伊拉克内战（2011年－至今）、叙利亚内战、利比亞內戰（2014年－至今） 、西奈半岛动乱和阿富汗戰爭 (2015年至今)，与各阿拉伯国家政府军[46][47]（也包括叙利亚反对派[48][49]）、部分地方武装以及一些北约成员国或欧洲国家军队交战[50][51][52][53][54][55][56][57][58]。2015年12月，伊斯蘭國宣稱要攻擊以色列[59]。该组织的几个领导人曾声称时任美国总统小布什2003年发动的伊拉克戰爭是导致他们发起对美国的圣战之原因，而美军行动使他们获得士兵和最终夺回国家的控制权变得容易[60] 。伊斯兰国并不谋求参与所佔領国家的政治权力分配，其根本目的是要在中东地区建立政教合一的極端伊斯兰国。伊斯兰国实行严格的伊斯兰教法，实现「伊斯兰化」，要讓受到統治的民眾「成為真正服從的穆斯林」。而从其在伊拉克和叙利亚采取的武装行动性质可以看出该组织極權主義、军国主义、伊斯蘭法西斯主義倾向十分明显。在萨达姆·海珊被美擒獲、阿拉伯之春後卡扎菲被打倒、阿萨德等泛阿拉伯世俗主义政权式微的現今，中东面临着回到逊尼派和什叶派宗教混战的危機。事实上，目前伊拉克政府军与反政府武装力量的对抗其中一部分就是一场逊尼派和什叶派的宗教混战。海灣逊尼派宗教神權國家（有別於世俗國家）與團體（沙特阿拉伯、卡達等）對什叶派國家的敵視，與對叛亂組織或明或暗的支持和資助（该组织大部分头目来自沙烏地阿拉伯），也是造成今日混亂局面的因素之一[61]。"
    result = extract_ne(texts)
    print "-----------\n"
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

    with open("./20170612data/zh/wiki/8191.txt") as f:
        result = extract_ne(f.read())
        print "-----------wiki zh\n"
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

    with open("./20170612data/zh/News/20104.zh.txt") as f:
        result = extract_ne(f.read())
        print "-----------News zh\n"
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

    with open("./20170612data/zh/dissertation/Safety/1600.zh.txt") as f:
        result = extract_ne(f.read())
        print "-----------Safe zh\n"
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

    with open("./20170612data/zh/dissertation/CIA/686.zh.txt") as f:
        result = extract_ne(f.read())
        print "-----------CIA zh\n"
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

    with open("./20170612data/zh/dissertation/Armedorganization/974.zh.txt") as f:
        result = extract_ne(f.read())
        print "-----------Armedorganization zh\n"
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
