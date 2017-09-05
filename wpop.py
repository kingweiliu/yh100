# coding=utf8

import urllib
import json

import  wordpress_xmlrpc
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from string import Template

# wp = Client('http://cy.syly8.com/xmlrpc.php', 'liujingwei', 'ljwisno1')
wp = Client('http://127.0.0.1/yh100/xmlrpc.php', 'liujingwei', 'ljwisno1')


post_template = u"""
<div>

<img style="float:right;width:180px"  src='$img'/>
商城名称：$shop<br/>
商品介绍: $introduce<br/>
原价: $origin_price <br/>
券值： $quan_price <br/>
现价: $now_price <br/>
购买连接：<a href=$tbk_link_quan>$tbk_link_quan</a>


</div>

"""


def push2wp(hotitem):
    format_cont = Template(post_template)
    # format_cont.substitute(shop = u"天猫", img=hotitem["goods_pic"])
    post = WordPressPost()
    post.title = hotitem["goods_title"]
    post.content = hotitem["goods_introduce"]
    iteminfo = json.dumps(hotitem)
    post.custom_fields = [{"key":"mall", "value" : hotitem["platform"]},
                          {"key":"url", "value":hotitem["tbk_link_quan"]},
                          {"key":"img", "value":hotitem["goods_pic"]},
                          {"key":"iteminfo", "value":iteminfo}]
    # post.thumbnail = hotitem["goods_pic"]

    post.content = format_cont.substitute(shop= hotitem["platform"].decode("utf8"),
                                          introduce = hotitem["goods_introduce"],
                                          origin_price = hotitem["origin_price"],
                                          quan_price = hotitem["zhekou_price"],
                                          now_price = float(hotitem["origin_price"]) - float(hotitem["zhekou_price"]),
                                          tbk_link_quan = hotitem["tbk_link_quan"],
                                          img=hotitem["goods_pic"])
    post.terms_names = {
        'post_tag': ['tagA', 'another tag'],
        'category': ['My Child Category'],
    }
    post.post_status = "publish"
    post.id = wp.call(wordpress_xmlrpc.methods.posts.NewPost(post))
    print post.id