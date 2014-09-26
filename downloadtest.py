# !/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import bs4
from bs4.element import NavigableString
from bs4.element import Tag
from bs4 import BeautifulSoup

import urllib2
import random

target_url = "http://www.douguo.com/caipu/zuixin/0"
caipu_url = "http://www.douguo.com/cookbook/958968.html"
caipu_url1 = "http://www.douguo.com/cookbook/178871.html"
caipu_url2 = "http://www.douguo.com/cookbook/996725.html"
caipu_url3 = "http://www.douguo.com/cookbook/179723.html"
caipu_url4 = "http://www.douguo.com/cookbook/996485.html"
http_type = "HTTPS"
proxy_ip = "183.221.217.162"
proxy_header = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

ZFLIAOFLAG = 0


def download_links(target_url):
    proxy = {http_type: proxy_ip}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    opener.addheaders.append(
        ('User-Agent', proxy_header)
    )
    content = opener.open(target_url)
    return content.getcode(), content


def analysize_content(content, links):
    soup = BeautifulSoup(content.read())
    list = soup.find_all("h3", class_="mts")
    for item in list:
        print item.getText().strip("\n").encode("utf-8")
        links.append(item.find("a").attrs["href"])


def return_code_judge(return_code, content, links):
    """
    通过content的getcode() 返回值判断网页内容是否获取成功
    :param return_code: content.getcode() 的返回值
    :param content:
    :param links: 全局的links
    :return: 成功返回1; 否则返回0
    """
    if return_code in [200, 206]:
        analysize_content(content, links)
        return 1
    else:
        return 0


def item_function(item, zudic, fudic):
    global ZFLIAOFLAG
    # zfliaoflag = 0
    zf_string = ''
    if isinstance(item, bs4.element.Tag):
        if item.has_attr("class"):
            # if 'mtim' in tlist1.attrs.get('class'):
            #     pass
            zf_string = item.find("td").getText().strip()
            # u'\u4e3b\u6599' is '主料'
            if zf_string == u'\u4e3b\u6599':
                ZFLIAOFLAG = 1
            # u'\u8f85\u6599' is '副料'
            elif zf_string == u'\u8f85\u6599':
                ZFLIAOFLAG = 2
            else:
                ZFLIAOFLAG = 0
            print zf_string
            print "ZFLIAOFLAG is %d" % ZFLIAOFLAG

        else:
            print "else ZFLIAOFLAG is %d" % ZFLIAOFLAG
            spanlist = item.findAll("span")
            num = len(spanlist)
            print num
            if num - 2 >= 0:
            # if num == 2:
                if (spanlist[0] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()
                elif (spanlist[0] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()

            if num == 4:
                # if (spanlist[0] is not u'') & (ZFLIAOFLAG is 1):
                #     zudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()
                # elif (spanlist[0] is not u'') & (ZFLIAOFLAG is 2):
                #     fudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()

                if (spanlist[2] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()
                elif (spanlist[2] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()

    # if item is '\n':
    #     continue

    print zudic
    print fudic


def analysize_cooking_step(cooking_step, stepdic):
    # 获取步骤和图片
    # 用于保存步骤和图片
    # stepdic = {}
    # 计数
    step_num = 0
    for single_step in cooking_step_list:
        step_discrible_pic = []
        # 步骤描述
        tlist = []
        step_num += 1

        step_discrible = single_step.find("p")
        for item in step_discrible.children:
            tlist.append(item)
        if len(tlist) >= 2:
            print tlist[1].strip()
            step_discrible_pic.append(tlist[1].strip())

        # 获取步骤描述对应的图片
        step_pic = single_step.find("a", class_="cboxElement")
        if step_pic is None:
            # 没有对应的描述图片，则对应的 href 为-1.
            print "没有对应的描述图片"
            step_discrible_pic.append(-1)
        else:
            print step_pic.__getitem__("href")
            step_discrible_pic.append(step_pic.__getitem__("href"))

        # 描述步骤和图片以 字典的形式保存
        # 如：
        # {1: ["步骤描述", "对应图片的href"]}
        stepdic[step_num] = step_discrible_pic

    print stepdic


# hero: comment
# 获取菜谱的对应id
PER_PAGE_NUM = 10
import json
comment_root_url = "http://www.douguo.com/ajax/getCommentsList/caipu/"


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


def connect_to_db():
    try:
        conn = MongoClient(host="localhost", port=27017)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = conn["douguo"]
    return dbh


if __name__ == '__main__':
    # links = []
    #
    # return_code, content = download_links(target_url)
    # if return_code_judge(return_code, content, links):
    #     print "download ok!"
    # else:
    #     print "%s is error!" % target_url

    # with open('/home/vipwp/liuquan/gitprograms/douguo/testx.html', 'w') as f:
    #     f.write(content.read())
    # print content.read()

    return_code, content = download_links(caipu_url1)

    # if return_code in [200, 206]:
    #     html = content.read()
    #
    # with open('/home/vipwp/liuquan/gitprograms/douguo/testcaipu.html', 'w') as f:
    #     f.write(html)
    soup = BeautifulSoup(content.read())
    #菜谱名称
    # caipu_name = soup.find("h1", id="page_cm_id").getText()
    caipu_name = soup.find("h1", id="page_cm_id").getText().encode("utf-8")
    print caipu_name
    #菜谱作者
    caipu_author_part = soup.find("div", class_="auhead").find("a")
    caipu_author_name = caipu_author_part.attrs["title"].encode("utf-8")
    caipu_author_link = caipu_author_part.attrs["href"]
    print caipu_author_name
    print caipu_author_link
    #菜谱story
    # caipu_story = soup.find("div", class_="xtip hidden", id="fullStory").getText().encode("utf-8")
    caipu_story = soup.find("div", class_="xtip hidden", id="fullStory")
    if caipu_story is not None:
        caipu_story = caipu_story.getText().encode('utf-8')
    else:
        caipu_story = -1
    print caipu_story


    # hero 菜谱照片
    cooking_pic_part = soup.find("div", class_="bmayi mbm")
    cooking_pic_url = cooking_pic_part.find(
        "a", class_="cboxElement", rel="recipe_img").__getitem__("href")
    print "a"
    #烹饪部分，该部分的table分离出来，对应的css属性为 class_="retew r3 pb25 mb20"
    #再逐个进行分解
    cooking = soup.find("div", class_="retew r3 pb25 mb20")
    cooking_part = cooking.find("table", class_="retamr")
    print "a"
    print "b"
    #烹饪难度
    cooking_diffcul_part = cooking_part.find("td", class_="lirre", width="50%")
    if cooking_diffcul_part is None:
        cooking_diffcul = -1
        cooking_time = -1
    else:
        difflist = []
        cookingtimelist = []
        #烹饪困难度
        for i in cooking_diffcul_part.children:
            difflist.append(i)
        if len(difflist) == 2:
            diffculity = difflist[1].strip()
            if diffculity == u'\u5207\u58a9(\u521d\u7ea7)':
                cooking_diffcul = 1
            elif diffculity == u'\u914d\u83dc(\u4e2d\u7ea7)':
                cooking_diffcul = 2
            else:
                cooking_diffcul = 3
        else:
            cooking_diffcul = -2

        if cooking_diffcul == 1:
            print "切墩(初级)"
        elif cooking_diffcul == 2:
            print "配菜(中级)"
        elif cooking_diffcul == 3:
            print "第三那种"
        else:
            print "未知"
        #烹饪时间
        for i in cooking_diffcul_part.next_siblings:
            cookingtimelist.append(i)
        if len(cookingtimelist) == 3:
            time_part = cookingtimelist[1].get_text().strip()
            if time_part == u'\u65f6\u95f4\uff1a10\u5206\u5de6\u53f3':
                cooking_time = 1
            elif time_part == u'\u65f6\u95f4\uff1a10-30\u5206\u949f':
                cooking_time = 2
            elif time_part == u'\u65f6\u95f4\uff1a30-60\u5206\u949f':
                cooking_time = 3
            elif time_part == u'\u65f6\u95f4\uff1a1\u5c0f\u65f6\u4ee5\u4e0a':
                cooking_time = 4
            else:
                cooking_time = 0
        else:
            cooking_time = -2

        if cooking_time == 1:
            print u'\u65f6\u95f4\uff1a10\u5206\u5de6\u53f3'
        elif cooking_time == 2:
            print u'\u65f6\u95f4\uff1a10-30\u5206\u949f'
        elif cooking_time == 3:
            print u'\u65f6\u95f4\uff1a30-60\u5206\u949f'
        elif cooking_time == 4:
            print u'\u65f6\u95f4\uff1a1\u5c0f\u65f6\u4ee5\u4e0a'
        else:
            print "wei zhi shijian"

    print "cooking_diffcul is %d" % cooking_diffcul
    print "cooking_time is %d" % cooking_time


    #烹饪主副料

    #烹饪主料
    list  = []
    zudic = {}
    fudic = {}
    for i in cooking_part:
        list.append(i)
    for item in list:
        item_function(item, zudic, fudic)
    print "final zudic is ", zudic
    print "final fudic is ", fudic

    for zukey in zudic.iterkeys():
        print zukey + ":",
        print zudic[zukey]

    print "-----"
    for fukey in fudic.iterkeys():
        print fukey + ":",
        print fudic[fukey]


    # 烹饪步骤
    cooking_step = cooking.find("div", class_="step clearfix")
    cooking_step_list = cooking_step.findAll("div", class_="stepcont mll libdm pvl clearfix")
    stepdic = {}
    analysize_cooking_step(cooking_step_list, stepdic)

    #小贴士
    xtieshi = ''
    xtieshi_content = cooking.find("div", class_="xtieshi")
    if xtieshi_content is not None:
        xtieshi = -1
    else:
        xtieshi = xtieshi_content.find("p").getText().strip()
    print xtieshi

    # hero: 标签
    taglist = []
    caipu_tag_part = soup.find("div", id="displaytag")
    if caipu_tag_part is not None:
        caipu_tag_list = caipu_tag_part.findAll("span")
        if len(caipu_tag_list) >= 1:
            for item in caipu_tag_list:
                taglist.append(item.getText().strip())
    print taglist

    # hero: 浏览，收藏
    watch_collect_part = soup.find("div", class_="falisc mbm")
    watch_collect_span = watch_collect_part.findAll("span", class_="fwb")
    watch_num = watch_collect_span[0].getText().strip()
    collect_num = watch_collect_span[1].getText().strip()

    # hero: 播放视频  video_url
    video_url_part = soup.find("div", class_="right mrl mtm fss fwn")
    if video_url_part is not None:
        video_url = video_url_part.__getitem__('href')
    else:
        video_url = -1

    # hero: author_url
    author_url_part = soup.find("div", class_="cpauthor clearfix mt46 pbs bbe7")
    author_url = author_url_part.find("div", class_="auhead").find("a").__getitem__("href")

    # hero: comment
    comment_dic = {}
    test_list = []
    get_comments(caipu_url1, comment_dic, test_list)
    test_set = set(test_list)
    print "a"
    print comment_dic
    print test_list
    print "list:", len(test_list)
    print "set:", len(test_set)




