# !/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re
from downsinglecaipu import download_per_caipu

target_url = "http://www.douguo.com/caipu/zuixin/30"
proxy_ip = "183.221.217.162"
proxy_header = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
http_type = "HTTPS"


def download_zx_per_page(target_url):
    proxy = {http_type: proxy_ip}
    proxy_surpport = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(proxy_surpport)
    opener.addheaders.append(
        ('User-Agent', proxy_header)
    )
    content = opener.open(target_url)
    return content.getcode(), content


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


if __name__ == '__main__':
    return_code, content = download_zx_per_page(target_url)
    perpage_caipu_list = []
    error_page_url = []
    if return_code in [200, 206]:
        get_perpage_caipu_list(content, perpage_caipu_list)
        if len(perpage_caipu_list) is 0:
            print "url或者解析有误"
            error_page_url.append(error_page_url)
        else:
            for per_caipu_url in perpage_caipu_list:
                download_per_caipu(per_caipu_url)
    else:
        print "下载有误！"


