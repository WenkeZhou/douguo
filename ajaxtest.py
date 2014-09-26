# !/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib2
import json
import random

PER_PAGE_NUM = 10

target_url = "http://www.douguo.com/cookbook/814268.html" 
aj_url = "/ajax/getCommentsList/caipu/814268/" 
ajall_url = "http://www.douguo.com/ajax/getCommentsList/caipu/814268/0"
aj_url = "http://www.douguo.com/cookbook/1037117.html"
ajall_url2 = "http://www.douguo.com/ajax/getCommentsList/caipu/1037117/0"

caipu_source_url = "http://www.douguo.com/cookbook/814268.html"


comment_root_url = "http://www.douguo.com/ajax/getCommentsList/caipu/"


# 获取菜谱的对应id
def get_caipu_id(url_test):
    caipu_id = url_test[url_test.find("book/")+5:url_test.find(".html")]
    return caipu_id


# 返回菜谱评论页数对应的 url
def get_comment_url(page_num, caipu_source_id):
    comment_url = comment_root_url + str(caipu_source_id) + "/" + str(page_num) + "?" + str(random.random())
    return comment_url

"""
对应返回json的格式
{u'data': {u'lists': [], u'total': 0, u'uinfo': {u'id': 0, u'info': []}},
 u'status': u'OK'}
"""

"""
{u'comment': u'\u8fd8\u4e0d\u9519 \u849c\u6709\u70b9\u7092\u7cca\u4e86',
 u'commentid': u'1200171',
 u'commenttype': u'0',
 u'cookid': u'814268',
 u'createdate': u'2014-07-04 14:18:30',
 u'createdate_hi': u'14:18',
 u'createdate_ymdhi': u'2014-07-04 14:18',
 u'flag': u'0',
 u'headicon': u'http://i1.douguo.net/static/img/48.jpg',
 u'imei': u'864690024098025',
 u'ip': u'0.0.0.0',
 u'local': u'',
 u'mac': u'd4:97:0b:49:26:e3',
 u'nickname': u'\u7ae0\u9c7c\u554a',
 u'parentid': u'0',
 u'purview': u'0',
 u'replyid': u'0',
 u'source': u"<a href='/page/appcenter' rel='nofollow' target='_blank' title='Android\u5ba2\u6237\u7aef'>Android\u5ba2\u6237\u7aef</a>",
 u'source_id': u'',
 u'source_url': u'',
 u't_headicon': u'http://i1.douguo.net/static/img/48.jpg',
 u't_nickname': u'',
 u't_username': u'',
 u'user_id': u'4620124',
 u'userid': u'4620124',
 u'username': u'u03001174250421',
 u'vipicon': False}
"""

# 模仿浏览器返回，返回ajax对应页数的信息
def get_content(target_url, ajax_url):
    """
    请求	GET
    http://www.douguo.com/ajax/getCommentsList/caipu/814268/0?0.6172902997118468 HTTP/1.1
    """
    my_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
            "Host": 'www.douguo.com',
            "Referer": target_url,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json; charset=utf-8"
    }
    """
     "GET":
     "http://www.douguo.com/cookbook/814268.html/ajax/getCommentsList/caipu/814268/10?0.5948076252825558 HTTP/1.1"
    """
    req = urllib2.Request(ajax_url, headers=my_headers)
    return urllib2.urlopen(req).read()


def get_page_num(total_num, per_page_num):
    pagenum = 0
    if (total_num / per_page_num == 0) & total_num > 0:
        pagenum = 1
        return pagenum
    elif total_num / per_page_num > 0:
        pagenum = total_num / per_page_num
        if total_num % per_page_num == 0:
            return pagenum
        else:
            return pagenum + 1
    else:
        return pagenum


def get_comments(source_url, comment_dic, test_list):
    caipu_source_id = get_caipu_id(source_url)
    ajax_url = get_comment_url(0, caipu_source_id)
    content = get_content(target_url, ajax_url)

    json_part = json.loads(content)
    data_part = json_part['data']
    lists_part = data_part['lists']
    total_num = data_part['total']
    total_page_num = 0
    total_page_num = get_page_num(total_num, PER_PAGE_NUM)
    if total_num == 0:
        pass
    else:
        for i in range(total_page_num):
            per_ajax_url = get_comment_url(i, caipu_source_id)
            per_content = get_content(target_url, per_ajax_url)
            per_lists_part = json.loads(per_content)['data']['lists']
            for j in range(len(per_lists_part)):
                comment_content = []
                comment_content.append(per_lists_part[j]["username"])
                comment_content.append(per_lists_part[j]["createdate"])
                test_list.append(per_lists_part[j]["username"])
                comment_dic[i*PER_PAGE_NUM + j] = comment_content


if __name__ == "__main__":
    comment_dic = {}
    test_list = []


    get_comments(target_url, comment_dic, test_list)
    test_set = set(test_list)
    print "a"
    print comment_dic
    print test_list
    print "list:", len(test_list)
    print "set:", len(test_set)