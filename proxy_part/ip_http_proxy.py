# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MrHero'

import urllib
import urllib2
from urllib2 import URLError, HTTPError
import random

import settings
import ip_lists
import user_agent_lists

import socket
socket.setdefaulttimeout(settings.SOCKET_TIME)

user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"


def direct_open(url):
    """
    直接打开url
    :param url:
    :return:
    """
    try:
        content = urllib2.urlopen(url)
        return content.getcode(), content
    except HTTPError, e:
        print "The server couldn't fullfill the request."
        print "Error code: %s" % e.code
        return -1, -1
    except URLError, e:
        print "We failed to reach a server."
        print "Reason: %s" % e.reason
        return -2, -2
    except socket.error, e:
        print "socket error" + e.message
        return -3, -3


def header_open(url, header_dict):
    """
    模仿浏览器
    :param url:
    :param user_agent: 浏览器的agent
    :return:
    """
    try:
        # my_headers = {
        #     'User-Agent': user_agent,
        #     'Host': 'www.douguo.com',
        #     'Referer': "http://www.douguo.com/cookbook/814268.html",
        #     "X-Requested-With": "XMLHttpRequest",
        #     "GET": ajall_url,
        #     "Content-Type": "application/json; charset=utf-8"
        # }
        req = urllib2.Request(url, headers=header_dict)
        content = urllib2.urlopen(req)
        return content.getcode(), content
    except HTTPError, e:
        print "The server couldn't fullfill the request."
        print "Error code: %s" % e.code
        return -1, -1
    except URLError, e:
        print "We failed to reach a server."
        print "Reason: %s" % e.reason
        return -2, -2
    except socket.error, e:
        print "socket error" + e.message
        return -3, -3


def ip_header_open(url, ip_dict, header_dict=None):
    try:
        ip = ip_dict['ip_adr']
        ip_type = ip_dict['type']
        ip_port = ip_dict['port']

        proxy = {ip_type: "%s:%s" % (ip, ip_port)}
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)

        if header_dict is None:
            content = opener.open(url)
        else:
            #方法一：
            req = urllib2.Request(url, headers=header_dict)
            content = opener.open(req)
            # #方法二：
            # urllib2.install_opener(opener)
            # req = urllib2.Request(url, headers=header_dict)
            # content = urllib2.urlopen(req)
        return content.getcode(), content
    except HTTPError, e:
        print "The server couldn't fullfill the request."
        print "Error code: %s" % e.code
        return -1, -1
    except URLError, e:
        print "We failed to reach a server."
        print "Reason: %s" % e.reason
        return -2, -2
    except socket.error, e:
        print "socket error" + e.message
        return -3, -3


def random_ip_header_open(url, my_headers=None):
    """
    用随机的ip 和 header组合, 打开指定url
    :param url:
    :return:
    """
    for _ in range(settings.TRY_OPEN_URL_MAX_TIMES):
        ip_dict = random.choice(ip_lists.ip_lists)
        user_agent = user_agent_lists.user_agent_lists[current]
        if my_headers is None:
            my_headers = {}
            my_headers["User-Agent"] = user_agent
        else:
            my_headers["User-Agent"] = user_agent
        result_code, content = ip_header_open(url, ip_dict, my_headers)
        if result_code in range(200, 206):
            return result_code, content
            break
        else:
            continue
    return result_code, content


if __name__ == '__main__':
    tar_url1 = "http://douguo.com"
    tar_url = "http://www.douguo.com/caipu/zuixin/266580"
    # get_code, content = direct_open_url(tar_url)
    my_headers = {
        "User-Agent": user_agent,
    }
    for i in range(69):
        get_code, content = random_ip_header_open(tar_url)


