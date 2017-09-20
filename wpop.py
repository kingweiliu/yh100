# coding=utf8

import urllib
import json
import time

import  wordpress_xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from string import Template

# wp = Client('http://cy.syly8.com/xmlrpc.php', 'liujingwei', 'ljwisno1')
# wp = Client('http://127.0.0.1/wordpress_yh/xmlrpc.php', 'liujingwei', 'ljwisno1')
wp = Client('http://yh.syly8.com/xmlrpc.php', 'liujingwei', 'ljwisno1')

post_template = u"""
<div>

<img style="float:right;width:180px"  src='$img'/>
商城名称：$shop<br/>
商品介绍: $introduce<br/>
原价: $origin_price <br/>
券值： $quan_price <br/>
现价: $now_price <br/>

</div>

"""


class yh100getkey(wordpress_xmlrpc.AnonymousMethod):
    method_name = 'yh100.getKey'
    method_args = ('number1',)

class yh100setkey(wordpress_xmlrpc.AnonymousMethod):
    method_name = 'yh100.setKey'
    method_args = ('key','value')

def yh100_getkey(key):
    oplist = wp.call(yh100getkey(key))
    return oplist

def yh100_setkey(key, v):
    oplist = wp.call(yh100setkey(key,v))
    print oplist
    return oplist

def check_exist(hotitem):
    """
    判断是否以前已经写入过
    :param hotitem:
    :return:

    """
    oplist =  wp.call(wordpress_xmlrpc.methods.options.GetOptions([]))
    for x in oplist:
        print x.name, x.value

def make_wp_content(hotitem):
    format_cont = Template(post_template)
    # format_cont.substitute(shop = u"天猫", img=hotitem["goods_pic"])
    post = WordPressPost()
    post.title = hotitem["goods_title"]
    post.content = hotitem["goods_introduce"]
    # post.post_type = "tbkitem"
    iteminfo = json.dumps(hotitem)
    post.custom_fields = [
                          {"key": "iteminfo", "value": iteminfo}]
    # post.thumbnail = hotitem["goods_pic"]

    post.content = format_cont.substitute(shop=hotitem["platform"].decode("utf8"),
                                          introduce=hotitem["goods_introduce"],
                                          origin_price=hotitem["origin_price"],
                                          quan_price=hotitem["zhekou_price"],
                                          now_price=float(hotitem["origin_price"]) - float(hotitem["zhekou_price"]),
                                          tbk_link_quan=hotitem["tbk_link_quan"],
                                          img=hotitem["goods_pic"])
    post.terms_names = {
        'post_tag': hotitem["tag"],
        'category': hotitem["category"],
    }
    post.post_status = "publish"
    return post

def calc_sign(hotitem):
    return hotitem["goods_id"] + "_" + hotitem["start_time"] + "_" + hotitem["end_time"]

def push2wp(hotitem):
    goods_id = hotitem["goods_id"]
    goods_record = yh100_getkey(goods_id)
    current_goods_sign = calc_sign(hotitem)
    post_id = None
    if goods_record:
        print goods_record
        goods_info = json.loads(goods_record[0]["meta_value"])
        print goods_info
        if current_goods_sign == goods_info["goods_sign"]:
            return 0

        post_id = goods_info["post_id"]
        post = wp.call(wordpress_xmlrpc.methods.posts.GetPost(post_id))

        iteminfo = json.dumps(hotitem)
        custom_fileds = {
            "iteminfo" : iteminfo
        }

        for index in range(len(post.custom_fields)):
            item_key = post.custom_fields[index]["key"]
            if item_key in custom_fileds:
                post.custom_fields[index]["value"] = custom_fileds[item_key]

        result = wp.call(wordpress_xmlrpc.methods.posts.EditPost(post_id, post))


    else:
        post = make_wp_content(hotitem)
        post_id = wp.call(wordpress_xmlrpc.methods.posts.NewPost(post))
    new_goods_info = {}
    new_goods_info["post_id"] = post_id
    new_goods_info["goods_sign"] = current_goods_sign
    new_goods_info["update_time"] = time.time()

    return yh100_setkey(hotitem["goods_id"], json.dumps(new_goods_info))

# yh100_setkey(1, 2)
print yh100_getkey(10)