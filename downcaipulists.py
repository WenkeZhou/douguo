# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
from downsinglecaipu import download_per_caipu
from dbpart import mongodbtest
from http_proxy_list import user_agent_list
from the_generate_ip_list import ip_list
import random


import socket
socket.setdefaulttimeout(8)

target_url = "http://www.douguo.com/caipu/zuixin/30"
proxy_ip = "183.221.217.162"
proxy_header = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
http_type = "HTTPS"


def download_zx_per_page(target_url):
    # user_agent = random.choice(user_agent_list)
    # item = random.choice(ip_list)
    # # {'ip_adr': u'183.221.56.185', 'type': u'HTTPS', 'port': u'8123', 'check_time': 0.06206116676330566},
    # ip = item['ip_adr']
    # ip_type = item['type']
    # port = item["port"]
    # proxy = {ip_type: "%s:%s" % (ip, port)}
    #
    #
    # # proxy = {http_type: proxy_ip}
    # proxy_surpport = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_surpport)
    # opener.addheaders.append(
    #     ('User-Agent', user_agent)
    # )

    content = ''
    for tries in range(5):
        try:
            user_agent = random.choice(user_agent_list)
            item = random.choice(ip_list)
            # {'ip_adr': u'183.221.56.185', 'type': u'HTTPS', 'port': u'8123', 'check_time': 0.06206116676330566},
            ip = item['ip_adr']
            ip_type = item['type']
            port = item["port"]
            proxy = {ip_type: "%s:%s" % (ip, port)}


            # proxy = {http_type: proxy_ip}
            proxy_surpport = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_surpport)
            opener.addheaders.append(
                ('User-Agent', user_agent)
            )

            content = opener.open(target_url)
            break
        except urllib2.URLError, e:
            if tries < 4:
                continue
            else:
                print "download_zx_per_page ip 链接有误!--->urllib2.URLError"
        except socket.error, e:
            if tries < 4:
                continue
            else:
                print "download_zx_per_page ip 链接超时!--->socket.error"

    if content == "":
        print "download_zx_per_page ip 链接有误!"
        return -1, -1
    elif content.getcode() in range(200, 207):
        return content.getcode(), content
    else:
        print "download_zx_per_page ip 链接有误!"
        return -1, -1
    # content = opener.open(target_url)
    # return content.getcode(), content


def get_perpage_caipu_list(content, perpage_caipu_list):
    html = content.read()
    soup = BeautifulSoup(html)
    target_html = soup.find_all("div", class_="course r5 col")
    for item in target_html:
        #itemlist 数据元素:
        #[caipu_url, caipu_author_url, caipu_created_time]
        #caipu_url:
        #caipu_author_url: -1,获取有误; url,获取正常
        itemlist = []

        # 获取菜谱链接
        caipu_url_part = item.find("div", class_="recpio")
        # for url_item in caipu_url_list:
        # perpage_caipu_list.append(item.find("a", attrs={"href":re.compile("http://www.douguo.com/cookbook/"")}))
        caipu_url_part2 = caipu_url_part.find("a", href=re.compile("http://www.douguo.com/cookbook/"))
        if caipu_url_part2 is not None:
            caipu_url = caipu_url_part2.__getitem__('href')
        else:
            caipu_url = -1

        itemlist.append(caipu_url)

        #获取菜谱时间和作者主页链接
        #caipu_author_url
        item_author_time = item.find("div", class_="cfabu clearfix")
        caipu_author_url_part = item_author_time.find("a", href=re.compile("http://www.douguo.com/u/"))
        if caipu_author_url_part is not None:
            caipu_author_url = caipu_author_url_part.__getitem__('href')
            itemlist.append(caipu_author_url)
        else:
            caipu_author_url = -1
            itemlist.append(caipu_author_url)

        #caipu_created_time
        caipu_created_time_part = item_author_time.find("p")
        if caipu_created_time_part is not None:
            try:
                caipu_created_time = caipu_created_time_part.get_text().strip()[-10:]
                itemlist.append(caipu_created_time)
            except Exception as ex:
                print ex
                caipu_created_time = -1
                itemlist.append(caipu_created_time)
        else:
            caipu_created_time = -1
            itemlist.append(caipu_created_time)

        # 如果 caipu_url is -1 则不加入到perpage_caipu_list 中
        if itemlist[0] != -1:
            perpage_caipu_list.append(itemlist)


# if __name__ == '__main__':
def down_per_page(target_url):
    # 下载该页的所有内容
    return_code, content = download_zx_per_page(target_url)
    perpage_caipu_list = []
    error_page_url = []
    if return_code in range(200, 206):
        get_perpage_caipu_list(content, perpage_caipu_list)
        if len(perpage_caipu_list) is 0:
            print "down_per_page url或者解析有误"
            error_page_url.append(target_url)
        else:
            for per_caipu_url in perpage_caipu_list:
                download_per_caipu(per_caipu_url)
    else:
        print "down_per_page 下载有误！"

    if len(error_page_url) > 0:
        error_page_url_set = set(error_page_url)
        dbh = mongodbtest.connect_to_db()
        dbh_collection_error_page_url = dbh.bad_page_url
        for item_url in error_page_url_set:
            if mongodbtest.whether_exist(dbh_collection_error_page_url, error_page_url=item_url):
                pass
            else:
                # dbh_collection_error_page_url.insert({
                #     "error_page_url": error_page_url
                # })
                mongodbtest.insert_bad_url(dbh_collection_error_page_url, bad_page_url=item_url)
        print "有 %d条页面没有成功获取，获取有误。" % len(error_page_url_set)



