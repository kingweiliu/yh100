# coding=utf8

import urllib
import json

import  wordpress_xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from string import Template

wp = Client('http://cy.syly8.com/xmlrpc.php', 'liujingwei', 'ljwisno1')


post_template = u"""
<div>

<img style="float:right;width:180px"  src='$img'/>
商城名称：$shop<br/>
商品介绍: $introduce<br/>
原价: $origin_price <br/>
券值： $quan_price <br/>
现价: $now_price <br/>
购买连接：<a href=$commission_link>$commission_link</a>


</div>

"""


def TestGetPost():
    wps = wp.call(wordpress_xmlrpc.methods.posts.GetPosts())
    for w in wps:
        print w.title
        print w.post_status

def push2wp(hotitem):
    format_cont = Template(post_template)
    # format_cont.substitute(shop = u"天猫", img=hotitem["goods_pic"])
    post = WordPressPost()
    post.title = hotitem["goods_title"]
    post.content = hotitem["goods_introduce"]
    post.thumbnail = hotitem["goods_pic"]
    print hotitem["commission_link"]
    post.content = format_cont.substitute(shop= u"天猫" if hotitem["is_tmall"] == 1 else u"淘宝",
                                          introduce = hotitem["goods_introduce"],
                                          origin_price = hotitem["goods_price"],
                                          quan_price = hotitem["coupon_price"],
                                          now_price = float(hotitem["goods_price"]) - float(hotitem["coupon_price"]),
                                          commission_link = hotitem["commission_link"][:30],

                                          img=hotitem["goods_pic"])
    post.terms_names = {
        'post_tag': hotitem["tag"],
        'category': hotitem["category"],
    }
    post.post_status = "publish"
    post.id = wp.call(wordpress_xmlrpc.methods.posts.NewPost(post))
    print post.id


def download_hot():
    f = urllib.urlopen("http://openapi.qingtaoke.com/baokuan?app_key=CdRk10ng&v=1.0")
    jshot = json.loads(f.read())
    if "er_code" in jshot and jshot["er_code"] == 10000:
        for x in jshot["data"]:
            print x["commission_type"]
            if ("commission_link" in x and not x["commission_link"]) or len(x["commission_link"]) < 10:
                continue
            print len(x["commission_link"])

            for y in x:
                print y, x[y]
            print x["goods_title"]
            # break
            push2wp(x)
            break


download_hot()