#-*-coding: utf-8-*-

import os
import commands
from flask import Flask, Response, render_template, request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
app = Flask(__name__)

def get_ins(target_root):
    if target_root == "发改委":
        command = "java -jar RecogIns.jar fagaiwei_search_results.txt %s %s 2 -1 -1" % (u"发改委,国家发改委,国家发展和改革委员会".encode("gbk"), u"司".encode("gbk"))
    elif target_root == "价格司":
        command = "java -jar RecogIns.jar jiagesi_search_results.txt %s %s -1 -1 -1" % (u"价格司".encode("gbk"), u"处".encode("gbk"))
    elif target_root == "伊斯兰":
        command = "java -jar RecogIns.jar islamstate_search_results.txt %s None 5 6 10" % u"伊斯兰,伊斯兰国".encode("gbk")
    else:
        return []
    print command
    process = os.popen(command)
    f = process.readlines()
    process.close()
    ins_dict = dict()
    father = ""
    if len(f):
        for line in f:
            text = line.strip().decode("gbk").encode("utf-8")
            if text == "":
                continue
            elif "#" in text:
                father = text.replace("#", "").replace("结果", "")
            else:

                try:
                    ins_dict[father].append(text)
                except KeyError:
                    ins_dict[father] = [text]
   
        process.close()
    else:
        with open("ins_result.txt") as f:
            for line in f:
                text = line.strip()
                if text == "":
                    continue
                elif "#" in text:
                    father = text.replace("#", "").replace("结果", "")
                else:

                    try:
                        ins_dict[father].append(text)
                    except KeyError:
                        ins_dict[father] = [text]

    results_dict = dict()
    middle_posfix = ["通讯社", "组织", "传媒社", "协会", "研究院", "产委会", "委员会", "协会", "研究会", "中心", "公司", "司", "所", "局", "处"]
    for fa, sons in ins_dict.iteritems():
        results = []
        resultset = set()
        if fa not in resultset:
            resultset.add(fa)
            results.append(fa)
        for son in sons:
            #print fa.decode("utf-8"), ":", son.decode("utf-8")
            ishit = False
            for pos in middle_posfix:
                if son.endswith(pos):
                    ishit = True
                    p1 = "%s.%s" % (fa, pos)
                    if p1 not in resultset:
                        results.append(p1)
                        resultset.add(p1)
                    p2 = "%s.%s.%s" % (fa, pos, son)
                    if p2 not in resultset:
                        results.append(p2)
                        resultset.add(p2)
            if not ishit:
                p3 = "%s.%s" % (fa, "其他")
                if p3 not in resultset:
                    results.append(p3)
                    resultset.add(p3)
                p4 = "%s.%s.%s" % (fa, "其他", son)
                if p4 not in resultset:
                    results.append(p4)
                    resultset.add(p4)
        results_dict[fa] = results

    try:
        resultslist = results_dict[target_root]
    except KeyError:
        resultslist = []

    return resultslist


@app.route('/flare.csv')
def generate_large_csv():
    def generate():
        with open("flare.csv") as f:
            for line in f:
                yield line.strip() + '\n'
 
    return Response(generate(), mimetype='text/csv')

@app.route('/')
def index():
    target = request.args.get("target", u"发改委")
    target = target.encode("utf-8")
    if target == "发改委":
        height = request.args.get("height", 2400)
    else:
        height = request.args.get("height", 900)
    width = request.args.get("width", 1400)
    
    layout = request.args.get("layout", "tree")
    if layout == "circle":
        height = request.args.get("height", 1800)
    
    resultlist = get_ins(target)
    resultlist2 = []
    if target == "发改委":
        resultlist1 = get_ins("价格司")
        prefix = ""
        for r in resultlist:
            data = r.split(".")
            if data[-1] == "价格司":
                prefix += ".".join(data[:len(data)-1])
                break
        for r1 in resultlist1:
            if r1 != "价格司":
                resultlist2.append(prefix + "." + r1)

    resultlist.extend(resultlist2)

    with open("flare.csv", "w") as fw:
        fw.write("%s,%s\n" % ("id", "value"))
        for r in resultlist:
            #print r.decode("utf-8")
            fw.write("%s,%s\n" % (r, 1))

    if len(resultlist):
        return render_template("demo.html", svg_width=width, svg_height=height, layout=layout)
    else:
        return "No data found!"


if __name__ == '__main__':
    app.run(debug=True)
    # 
    # 
    # 