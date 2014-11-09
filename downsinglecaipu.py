# !/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import hashlib
import os
import random
import bs4
from bs4.element import NavigableString
from bs4.element import Tag
from bs4 import BeautifulSoup
import urllib2
from dbpart import mongodbtest
import json
from http_proxy_list import user_agent_list
from the_generate_ip_list import ip_list

from proxy_part.ip_http_proxy import random_ip_header_open
import socket

socket.setdefaulttimeout(8)


PER_PAGE_NUM = 10
comment_root_url = "http://www.douguo.com/ajax/getCommentsList/caipu/"
CAIKU_ROOT_PATH1 = "/Users/vipwp/liuquan/gitprograms/douguopic/upload/caiku"
CAIKU_ROOT_PATH = "smb://192.168.11.148/herofile/"
target_url = "http://www.douguo.com/cookbook/178871.html"
ZFLIAOFLAG = 0


http_type = "HTTPS"
proxy_ip = "183.221.217.162"
proxy_header = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


def download_links(target_url):
    """
    下载target_url 的网页包
    :param target_url: 所要下载的链接
    :return: return_code: 打开target_url 的状态码; content: target_url 对应的网页包
    """
    user_agent = random.choice(user_agent_list)
    item = random.choice(ip_list)
    # {'ip_adr': u'183.221.56.185', 'type': u'HTTPS', 'port': u'8123', 'check_time': 0.06206116676330566},
    ip = item['ip_adr']
    ip_type = item['type']
    port = item["port"]
    proxy = {ip_type: "%s:%s" % (ip, port)}

    # proxy = {http_type: proxy_ip}
    proxy_support = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_support)
    opener.addheaders.append(
        ('User-Agent', user_agent)
    )

    content = ''
    for tries in range(5):
        try:
            content = opener.open(target_url)
            break
        except urllib2.URLError, e:
            if tries < 4:
                continue
            else:
                print "该download_links ip 链接有误!--->urllib2.URLError"

        except socket.error, e:
            if tries < 4:
                continue
            else:
                print "该download_links ip 链接超时!--->socket.error"

    if content == "":
        print "该download_links ip 链接有误!222"
        return -1, -1
    elif content.getcode() in range(200, 207):
        return content.getcode(), content
    else:
        print "该download_links ip 链接有误!"
        return -1, -1

    # content = opener.open(target_url)
    # return content.getcode(), content


def get_caipu_name(soup):
    """
    获取菜谱名称
    :param soup:
    :return: 菜谱名称
    """
    caipu_name = soup.find("h1", id="page_cm_id").getText().encode("utf-8")
    return caipu_name


def get_caipu_author(soup):
    """
    获取菜谱作者(url)
    :param soup:
    :return: 菜谱作者nickname 和 对应的链接
    """
    caipu_author_part = soup.find("div", class_="auhead").find("a")
    caipu_author_nickname = caipu_author_part.attrs["title"].encode("utf-8")
    caipu_author_url = caipu_author_part.attrs["href"]
    return caipu_author_nickname, caipu_author_url


def get_caipu_pic(soup, author_nickname, caipu_name):
    """
    获取菜谱成品照片
    :param soup:
    :param salt: 对生成的文件名进行加盐，加盐方式为 caipu_name, "hero"
    :return: 菜谱成品照片的保存路径, 图片下载失败，则返回-1
    路径格式为:
    upload/caiku/nickname(md5)/salt(图片种类+caipu_name+hero*防重复).pic
    """

    caipu_pic_part = soup.find("div", class_="bmayi mbm")
    caipu_pic_url = caipu_pic_part.find(
        "a", class_="cboxElement", rel="recipe_img").__getitem__("href")

    #获取 该图片下载路径 对应的文件名后缀
    suffix_part = caipu_pic_url[-10:]
    suffix_dot_position = suffix_part.find(".")
    pic_suffix = suffix_part[-suffix_dot_position:]

    # 参照路径格式， nickname(md5) 对应的md5
    nickname_md5 = hashlib.new('md5', author_nickname).hexdigest()

    # 参照路径格式， salt(图片种类+caipu_name+hero*防重复) 对应的md5
    # 图片种类: 成品("chengpin")，菜谱制作步骤("step"), 用户头像("user_photo_small"),
    #         用户头像("user_photo_big"),
    salt = "chengpin" + caipu_name + "hero"

    caipu_name_salt_md5 = hashlib.new('md5', salt).hexdigest()
    # 参照路径格式，nickname 对应的目录
    caipu_root_path_nickname = os.path.join(CAIKU_ROOT_PATH, nickname_md5)

    # 如果该路径不存在，则创建 caipu_root_path_nickname 命名的文件夹
    if os.path.isdir(caipu_root_path_nickname) is False:
        os.makedirs(caipu_root_path_nickname)

    # 存在该 caipu_author_nickname 目录，就把对应的图片下载进来
    caipu_root_path_salt = os.path.join(caipu_root_path_nickname, caipu_name_salt_md5)
    i = 1
    # 如果有重复的图片，则继续加盐,加盐规则: next_salt = salt + "%d“ % i
    while os.path.isfile(caipu_root_path_salt+suffix_part):
        next_salt = salt + "_%d" % i
        caipu_name_salt_md5 = hashlib.new('md5', next_salt).hexdigest()
        caipu_root_path_salt = os.path.join(caipu_root_path_nickname, caipu_name_salt_md5)
        i += 1
    #下载该图片
    try:
        # urllib.urlretrieve(caipu_pic_url, caipu_root_path_salt+pic_suffix)
        # print "下载图片"
        pass
    except Exception as ex:
        print ex
        #下载图片失败，则返回1，并将下载的图片删除掉，因为下载的图片很有可能打不开，无用
        if os.path.isfile(ccaipu_root_path_salt+pic_suffix):
            os.remove(caipu_root_path_salt+pic_suffix)
        return -1
    return caipu_root_path_salt + pic_suffix


def get_caipu_story(soup):
    """
    获取菜谱的描述部分
    :param soup:
    :return: 以"utf-8"的字符串形式返回。如果菜谱的描述部分为空，则返回-1
    """
    caipu_story = soup.find("div", class_="xtip hidden", id="fullStory")
    if caipu_story is not None:
        caipu_story = caipu_story.getText().encode('utf-8')
    else:
        caipu_story = -1
    return caipu_story


def get_caipu_diffcul_time(cooking_part):
    """
    获取菜谱的烹饪难度
    :param cooing_part:
    :return:
    cooking_diffcul: -1,没有配置烹饪难度; 1,配菜(初级); 2,切墩(中级); 3,掌勺(高级); -2,获取出错
    cooking_time: -1,没有配置烹饪时长; 1,10分钟左右; 2,10~30分钟; 3,30~60分钟; 4,1小时以上; -2,获取出错
    """
    cooking_diffcul = -1
    cooking_time = -1
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
            elif diffculity == u'\u638c\u52fa(\u9ad8\u7ea7)':
                cooking_diffcul = 3
        else:
            cooking_diffcul = -2

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
                cooking_time = -2
        else:
            cooking_time = -2

    return cooking_diffcul, cooking_time


def item_function(item, zudic, fudic):
    global ZFLIAOFLAG
    zf_string = ''
    if isinstance(item, bs4.element.Tag):
        if item.has_attr("class"):
            zf_string = item.find("td").getText().strip()
            # u'\u4e3b\u6599' is '主料'
            if zf_string == u'\u4e3b\u6599':
                ZFLIAOFLAG = 1
            # u'\u8f85\u6599' is '副料'
            elif zf_string == u'\u8f85\u6599':
                ZFLIAOFLAG = 2
            else:
                ZFLIAOFLAG = 0

        else:
            spanlist = item.findAll("span")
            num = len(spanlist)
            if num - 2 >= 0:
                if (spanlist[0] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()
                elif (spanlist[0] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()

            if num == 4:
                if (spanlist[2] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()
                elif (spanlist[2] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()


def get_caipu_zuliao(cooking_part, caipu_zuliao, caipu_fuliao):
    """
    获取菜谱主料，副料
    :param cooking_part:
    :param caipu_zuliao:
    :param caipu_fuliao:
    :return: 主料,副料为空则表示没有对其进行配置
    """
    list = []
    for i in cooking_part:
        list.append(i)
    for item in list:
        item_function(item, caipu_fuliao, caipu_fuliao)


def analysize_cooking_step(cooking_step_list, stepdic, author_nickname, caipu_name):
    """
    获取步骤和图片
    :param cooking_step_list:
    :param stepdic: 用于保存步骤和图片
    :param author_nickname: 作品的作者
    :param caipu_name: 菜谱的名称
    :return:
    """
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
            step_discrible_pic.append(tlist[1].strip())

        # 获取步骤描述对应的图片
        step_pic = single_step.find("a", class_="cboxElement")
        if step_pic is None:
            # 没有对应的描述图片，则改部分图片的 path 为0, url 为 0.
            # print "没有对应的描述图片"
            step_discrible_pic.append(0)
            step_discrible_pic.append(0)
        else:
            step_pic_url = step_pic.__getitem__("href")
            caipu_step_pic_path, return_result = caipu_step_download_pic(step_pic_url, author_nickname, caipu_name)
            if return_result == 1:
                step_discrible_pic.append(caipu_step_pic_path)
                step_discrible_pic.append(step_pic_url)
            elif return_result == -1:
                #图片链接有问题，下载失败，则返回路径为-1，已提供在分析。并返回改图片的url
                step_discrible_pic.append(-1)
                step_discrible_pic.append(step_pic_url)

        # 描述步骤和图片以 字典的形式保存
        # 如：
        # {1: ["步骤描述", "对应图片的路径", "对应图片的下载链接"]}
        # {Num: ["step describe", "path", "url"]}
        # Num: 表示操作步骤编号
        # path: 0,表示没有提供图片; -1, 表示下载出错;
        # url: 0,表示没有提供图片; "url",表示提供的图片下载链接，以供后续分析;
        stepdic[str(step_num)] = step_discrible_pic


def caipu_step_download_pic(step_pic_url, author_nickname, caipu_name):
    """
    下载每一步描述对应的图片
    :param step_pic_url:
    :return: 图片下载失败，则返回-1,-1; 如果下载成功，则返回图片path,1.
    路径格式为:
    upload/caiku/nickname(md5)/salt(图片种类+caipu_name+hero*防重复).pic
    """
    return_result = 0
    #获取 该图片下载路径 对应的文件名后缀
    suffix_part = step_pic_url[-10:]
    suffix_dot_position = suffix_part.find(".")
    pic_suffix = suffix_part[-suffix_dot_position:]

    # 参照路径格式， nickname(md5) 对应的md5
    nickname_md5 = hashlib.new('md5', author_nickname).hexdigest()

    # 参照路径格式， salt(图片种类+caipu_name+hero*防重复) 对应的md5
    # 图片种类: 成品("chengpin")，菜谱制作步骤("step"), 用户头像("user_photo_small"),
    #         用户头像("user_photo_big"),
    salt = "step" + caipu_name + "hero"

    caipu_name_salt_md5 = hashlib.new('md5', salt).hexdigest()
    # 参照路径格式，nickname 对应的目录
    caipu_root_path_nickname = os.path.join(CAIKU_ROOT_PATH, nickname_md5)

    # 如果该路径不存在，则创建 caipu_root_path_nickname 命名的文件夹
    if os.path.isdir(caipu_root_path_nickname) is False:
        os.makedirs(caipu_root_path_nickname)

    # 存在该 caipu_author_nickname 目录，就把对应的图片下载进来
    caipu_root_path_salt = os.path.join(caipu_root_path_nickname, caipu_name_salt_md5)
    i = 1
    # 如果有重复的图片，则继续加盐,加盐规则: next_salt = salt + "%d“ % i
    while os.path.isfile(caipu_root_path_salt+suffix_part):
        next_salt = salt + "_%d" % i
        caipu_name_salt_md5 = hashlib.new('md5', next_salt).hexdigest()
        caipu_root_path_salt = os.path.join(caipu_root_path_nickname, caipu_name_salt_md5)
        i += 1
    #下载该图片
    try:
        # urllib.urlretrieve(step_pic_url, caipu_root_path_salt+pic_suffix)
        return_result = 1
    except Exception as ex:
        print ex
        #下载图片失败，则返回-1，并将下载的图片删除掉，因为下载的图片很有可能打不开，无用。
        if os.path.isfile(caipu_root_path_salt+pic_suffix):
            os.remove(caipu_root_path_salt+pic_suffix)
        return_result = -1
        # caipu_root_path_salt + pic_suffix = -1
        caipu_root_path_salt = -1
        pic_suffix = 0

    return caipu_root_path_salt + pic_suffix, return_result


def get_caipu_tips(cooking):
    """
    获取小贴士
    :param cooking:
    :return: -1, 没有设置小贴士，小贴士为空; -2, 返回小贴士对应的字符串
    """
    xtieshi = ''
    xtieshi_content = cooking.find("div", class_="xtieshi")
    if xtieshi_content is not None:
        xtieshi = -1
    else:
        try:
            xtieshi = xtieshi_content.find("p").getText().strip()
        except Exception as ex:
            xtieshi = -1
            pass
    return xtieshi


def get_caipu_tags(soup, taglist):
    """
    获取菜谱标签
    :param soup:
    :param taglist:
    :return: taglist 为空 表示没有设置tag.
    """
    caipu_tag_part = soup.find("div", id="displaytag")
    if caipu_tag_part is not None:
        caipu_tag_list = caipu_tag_part.findAll("span")
        if len(caipu_tag_list) >= 1:
            for item in caipu_tag_list:
                taglist.append(item.getText().strip())


def get_caipu_video_url(soup):
    """
    获取菜谱视频播放链接
    :param soup:
    :return: -1, 表示没有对应的播放视屏链接
    """
    video_url_part = soup.find("div", class_="right mrl mtm fss fwn")
    if video_url_part is not None:
        video_url = video_url_part.__getitem__('href')
    else:
        video_url = -1
    return video_url


def get_caipu_id(url_test):
    """
    :return: 返回该菜谱对应的id号
    """
    caipu_id = url_test[url_test.find("book/")+5: url_test.find(".html")]
    return caipu_id


def get_comment_url(page_num, caipu_source_id):
    """
    :param page_num
    :param caipu_source_id
    :return : 返回请求服务器 所需的评论的 url
    """
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


def get_content(target_url, ajax_url):
    user_agent = random.choice(user_agent_list)
    """
    模仿浏览器返回，返回当前页对应的ajax的信息
    :param target_url: 当前页对应的url
    :param ajax_url:
    :return:
    """
    """
    请求	GET
    http://www.douguo.com/ajax/getCommentsList/caipu/814268/0?0.6172902997118468 HTTP/1.1
    """
    my_headers = {
            'User-Agent': user_agent,
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

    content = ''
    try:
        content = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print "该ajax ip 链接有误!--->urllib2.URLError"
    except socket.error, e:
        print "该ajax  ip 链接超时!--->socket.error"
    finally:
        if content == "":
            print "该ajax ip 链接有误!222"
            return -1
        elif content.getcode() in range(200, 207):
            return content.read()
        else:
            print "该ajax ip 链接有误!"
            return -1
    # return urllib2.urlopen(req).read()


def get_page_num(total_num, per_page_num):
    """
    获得评论的页数
    :param total_num: 总品论量
    :param per_page_num: 每页的评论数
    :return: 评论的页数
    """
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


def get_caipu_comments(source_url, comment_dic, dbh):
    """
    获取菜谱对应的评论
    :param source_url:
    :param comment_dic:
    :return: comment_dic --> {}
    对应的格式为：{
     评论标号: [评论人用户id, 评论时间],
     0: [u'u41207731650711', u'2012-08-02 17:52:34'],
     1: [u'u44077512467791', u'2012-08-04 18:56:26']
    }
    """
    caipu_source_id = get_caipu_id(source_url)
    ajax_url = get_comment_url(0, caipu_source_id)
    my_headers = {
            "Host": 'www.douguo.com',
            "Referer": target_url,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json; charset=utf-8"
    }
    content = get_content(ajax_url)

    if content not in (-1, -2, -3):
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

                if per_content != -1:
                    per_lists_part = json.loads(per_content)['data']['lists']
                    for j in range(len(per_lists_part)):
                        comment_content = []
                        comment_content.append(per_lists_part[j]["username"])
                        comment_content.append(per_lists_part[j]["createdate"])
                        comment_dic[str(i*PER_PAGE_NUM + j)] = comment_content
    else:
        mongodbtest.insert_bad_url(dbh.bad_comment_url, bad_comment_url=source_url)


"""
/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python /Users/vipwp/liuquan/gitprograms/douguo/downcaipulists.py
该菜谱对应的链接没有入库
http://www.douguo.com/cookbook/1044948.html
'NoneType' object has no attribute 'find'
该菜谱对应的链接没有入库
http://www.douguo.com/cookbook/1044947.html
没有对应的描述图片
没有对应的描述图片
没有对应的描述图片
没有对应的描述图片
'NoneType' object has no attribute 'find'
该菜谱对应的链接没有入库
http://www.douguo.com/cookbook/1044946.html
该菜谱对应的链接没有入库
http://www.douguo.com/cookbook/1044945.html
'NoneType' object has no attribute 'find'
该菜谱对应的链接没有入库
http://www.douguo.com/cookbook/1044944.html
'NoneType' object has no attribute 'find'
"""

# if __name__ == '__main__':


def download_per_caipu(per_caipu_url):
    # 返回数据库链接
    dbh = mongodbtest.connect_to_db()
    # if dbh.caipuku.find({"caipu_url": per_caipu_url[0]}).count() != 0:
    dbh_coll_caipuku = dbh.caipuku
    if mongodbtest.whether_exist(dbh_coll_caipuku, caipu_url=per_caipu_url[0]):
        print "该菜谱对应的链接已经入库"
    else:
        print "该菜谱对应的链接没有入库"
        print per_caipu_url[0]
        return_code, content = random_ip_header_open(per_caipu_url[0])
        if return_code not in range(200, 207):
            print "Can't not get back %s" % per_caipu_url[0]
            mongodbtest.insert_bad_url(dbh.error_download_caipu_url, caipu_url=per_caipu_url[0])
            # dbh.error_download_caipu_url.insert({
            #     "caipu_url": per_caipu_url[0],
            # }, safe=True)
        else:
            try:
                soup = BeautifulSoup(content.read())
                #开始分析soup,并将结果保存到数据库对应的菜谱表中

                # herotag 获取菜谱名称
                caipu_name = get_caipu_name(soup)

                # herotag 获取作者nickname，url
                caipu_author_nickname, caipu_author_url = get_caipu_author(soup)

                # herotag 获取成品照片, 下载并返回所在路径
                caipu_pic_path = get_caipu_pic(soup, caipu_author_nickname, caipu_name)

                # herotag 获取菜谱story
                caipu_story = get_caipu_story(soup)

                # herotag 获取菜谱浏览量(caipu_pageview) 和 收藏量(caipu_collection)
                watch_collect_part = soup.find("div", class_="falisc mbm")
                watch_collect_span = watch_collect_part.findAll("span", class_="fwb")
                caipu_pageview = watch_collect_span[0].getText().strip()
                caipu_collection = watch_collect_span[1].getText().strip()


                #烹饪部分，该部分的table分离出来，对应的css属性为 class_="retew r3 pb25 mb20"
                #再逐个进行分解
                cooking = soup.find("div", class_="retew r3 pb25 mb20")
                cooking_part = cooking.find("table", class_="retamr")

                # herotag 获取菜谱烹饪难度
                caipu_diffcul, caipu_time = get_caipu_diffcul_time(cooking_part)

                # herotag 获取菜谱主料,副料
                caipu_zuliao = {}
                caipu_fuliao = {}
                get_caipu_zuliao(cooking_part, caipu_zuliao, caipu_fuliao)

                # for zukey in caipu_zuliao.iterkeys():
                #     print zukey + ":",
                #     print caupu_zuliao[zukey]
                #
                # print "-----"
                # for fukey in caipu_fuliao.iterkeys():
                #     print fukey + ":",
                #     print caipu_fuliao[fukey]

                # herotag 获取菜谱描述步骤，以及对应图片
                # 烹饪步骤
                cooking_step = cooking.find("div", class_="step clearfix")
                cooking_step_list = cooking_step.findAll("div", class_="stepcont mll libdm pvl clearfix")
                caipu_step = {}
                analysize_cooking_step(cooking_step_list, caipu_step, caipu_author_nickname, caipu_name)

                # herotag 小贴士
                caipu_tips = get_caipu_tips(cooking)

                # herotag 标签
                caipu_tags = []
                get_caipu_tags(soup, caipu_tags)

                # herotag 创建时间
                caipu_created_time = per_caipu_url[2]

                # herotag 在线烹饪视屏链接
                caipu_video_url = get_caipu_video_url(soup)

                # herotag 评论
                caipu_comment_id = {}
                get_caipu_comments(target_url, caipu_comment_id, dbh)


                # print type(target_url)
                # print type(caipu_name)
                # print type(caipu_author_url)
                # print type(caipu_pic_path)
                # print type(caipu_story)
                # print type(caipu_pageview)
                # print type(caipu_collection)
                # print type(caipu_diffcul)
                # print type(caipu_time)
                # print type(caipu_zuliao)
                # print type(caipu_fuliao)
                # print type(caipu_step)
                # print type(caipu_tips)
                # print type(caipu_video_url)
                # print type(caipu_comment_id)

                #将获取的数据插入数据库dbh中
                dbh.caipuku.insert({
                    "caipu_url": per_caipu_url[0],
                    "caipu_name": caipu_name,
                    "caipu_author_url": caipu_author_url,
                    "caipu_pic_path": caipu_pic_path,
                    "caipu_story": caipu_story,
                    "caipu_pageview": caipu_pageview,
                    "caipu_collection": caipu_collection,
                    "caipu_diffcul": caipu_diffcul,
                    "caipu_time": caipu_time,
                    "caipu_zuliao": caipu_zuliao,
                    "caipu_fuliao": caipu_fuliao,
                    "caipu_step": caipu_step,
                    "caipu_tips": caipu_tips,
                    "caipu_created_time": caipu_created_time,
                    "caipu_video_url": caipu_video_url,
                    "caipu_comments": caipu_comment_id
                }, safe=True)
            except Exception as ex:
                print "Big erro!"
                print per_caipu_url[0]
                mongodbtest.insert_bad_url(dbh.error_download_caipu_url, caipu_url=per_caipu_url[0])
                # dbh.error_download_caipu_url.insert({
                #     "caipu_url": per_caipu_url[0],
                # }, safe=True)
