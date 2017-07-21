#-*-coding: utf-8-*-

import os
import json
import commands
from flask import Flask, Response, render_template, request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

def get_ins(target_root):
    if target_root == "发改委":
        command = "java -jar RecogSubsidiaries.jar first"
    elif target_root == "价格司":
        command = "java -jar RecogSubsidiaries.jar second %s" % u"价格司".encode("gbk")
    elif target_root == "经济运行调节局":
        command = "java -jar RecogSubsidiaries.jar second %s" % u"经济运行调节局".encode("gbk")
    else:
        return []
    print command
    process = os.popen(command)
    f = process.readlines()
    process.close()
    ins_dict = dict()
    father = target_root
    if len(f):
        for line in f:
            text = line.strip().decode("gbk").encode("utf-8")
            if text == "":
                continue
            elif "=" in text:
                middle_node = text.replace("=", "")
            else:
                try:
                    ins_dict[middle_node].append(text)
                except KeyError:
                    ins_dict[middle_node] = [text]
   
        process.close()

    results_dict = {"name": father, "children": []}
    middle_posfix = ["厅", "司", "局", "办公室", "协会", "中心"]
    rest_posfix = list(set(ins_dict.keys()) - set(middle_posfix))
    middle_posfix += rest_posfix
    for m in middle_posfix:
        try:
            children = ins_dict[m]
        except KeyError:
            continue
        children = [{"name": c, "size": 1} for c in children]
        results_dict["children"].append({"name": m, "children": children})

    return results_dict


@app.route('/flare.json')
def generate_json():
    string = ""
    with open("flare.json") as f:
        string = f.read()
 
    return Response(string, mimetype='text/json')

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

    results_dict = get_ins(target)
    if target == "发改委":
        results_dict1 = get_ins("价格司")
        results_dict2 = get_ins("经济运行调节局")
        for child in results_dict["children"]:
            if child["name"] == "司":
                for child1 in child["children"]:
                    if child1["name"] == "价格司":
                        child1.update(results_dict1)
            elif child["name"] == "局":
                for child1 in child["children"]:
                    if child1["name"] == "经济运行调节局":
                        child1.update(results_dict2)
    with open("flare.json", "w") as fw:
        fw.write("%s\n" % json.dumps(results_dict))

    if len(results_dict) > 0:
        return render_template("demo20170721.html", svg_width=width, svg_height=height, layout=layout)
    else:
        return "No data found!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
