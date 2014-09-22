# !/usr/bin/env python
# -*- coding: utf-8 -*-

import bs4
from bs4.element import NavigableString
from bs4.element import Tag
from bs4 import BeautifulSoup

import urllib2


target_url = "http://www.douguo.com/caipu/zuixin/0"
caipu_url = "http://www.douguo.com/cookbook/958968.html"
caipu_url1 = "http://www.douguo.com/cookbook/178871.html"
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
            if num == 2:
                if (spanlist[0] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()
                elif (spanlist[0] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()

            if num == 4:
                if (spanlist[0] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()
                elif (spanlist[0] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[0].getText().strip()] = spanlist[1].getText().strip()

                if (spanlist[2] is not u'') & (ZFLIAOFLAG is 1):
                    zudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()
                elif (spanlist[2] is not u'') & (ZFLIAOFLAG is 2):
                    fudic[spanlist[2].getText().strip()] = spanlist[3].getText().strip()

    # if item is '\n':
    #     continue

    print zudic
    print fudic




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
            else:
                cooking_diffcul = 2
        else:
            cooking_diffcul = -2

        #烹饪时间
        for i in cooking_diffcul_part.next_siblings:
            cookingtimelist.append(i)
        if len(cookingtimelist) == 3:
            time_part = cookingtimelist[1].get_text().strip()
            if time_part == u'\u65f6\u95f4\uff1a10-30\u5206\u949f':
                cooking_time = 2
            else:
                cooking_time = 1
        else:
            cooking_time = -2

    print "cooking_diffcul is %d" % cooking_diffcul
    print "cooking_time is %d" % cooking_time



    #烹饪主副料

    #烹饪主料
    list  = []
    zudic = {}
    fudic = {}
    # global ZFLIAOFLAG
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