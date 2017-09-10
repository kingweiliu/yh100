# coding: utf-8
import csv
import sys
import re
import json
import urllib

import wpop

def find_zhekou(text):
    pat = "[^\d]+(\d+)[^\d]+(\d+)"
    pat2= "\d+"
    print text
    # 满58元减20元
    mm = re.match(pat, text) 
    if mm:
        return (int(mm.group(2)), int(mm.group(1)))
    else: 
        # 5元无条件券
        mm = re.match(pat2, text)
        if mm:
            return (int(mm.group(0)), 0)
    return (0, 0)

def get_qtk_info(gid):
    target_url = "http://openapi.qingtaoke.com/search?s_type=1&key_word="+ gid +"&app_key=CdRk10ng&v=1.0"
    f = urllib.urlopen(target_url)
    jshot = json.loads(f.read())
    if "er_code" in jshot and jshot["er_code"] == 10000 and jshot["data"]["total"] == 1:
        return jshot["data"]["list"][0]
    return None

def load_csv(filename):
    with open(filename, "rb") as csvfile:
        csvreader = csv.reader(csvfile)
        csvreader.next()
        for x in csvreader:
            tbkitem = {}
            tbkitem["goods_id"] = x[0]

            # qtk_info = get_qtk_info(x[0])
            # if not qtk_info:
            #     continue
            # tbkitem["goods_introduce"] = qtk_info["goods_introduce"]
            # tbkitem["goods_short_title"] = qtk_info["goods_short_title"]

            tbkitem["goods_introduce"] = ""
            tbkitem["goods_short_title"] = ""

            tbkitem["goods_title"] = x[1]
            tbkitem["goods_pic"] = x[2]
            print x[2]
            tbkitem["goods_cat"] = x[4]
            tbkitem["tbk_link"] = x[5]
            tbkitem["origin_price"] = float(x[6])
            zhekou, condition_price = find_zhekou(x[17])
            tbkitem["zhekou_price"] = zhekou
            tbkitem["platform"] = x[13]
            tbkitem["start_time"] = x[18]
            tbkitem["end_time"] = x[19]
            tbkitem["tbk_link_quan"] = x[21]


            print wpop.push2wp(tbkitem)
           #  print tbkitem["goods_title"]
            # for y in tbkitem:
            #    print y, tbkitem[y]

            break
    pass




if __name__ == "__main__":
    load_csv("abc.csv")
