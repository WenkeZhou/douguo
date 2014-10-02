# !/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import sys


# 链接数据库
def connect_to_db():
    """
    链接数据库.
    douguotest 为测试数据库
    herodouguo 为正式数据库
    :return: 数据库链接
    """
    try:
        conn = MongoClient(host="localhost", port=27017)
    except ConnectionFailure, e:
        sys.stderr.write("Could not connect to the MongoDB: %s" % e)
        sys.exit(1)
    dbh = conn["douguotest"]
    return dbh


# 查询是否有该值
def whether_exist(dbh, **kwargs):
    """
    查询是否有查询的的值
    :param dbh:
    :param collection:
    :param **kwargs:
    :return: 如果存在所要查询值，则返回True; 否则，返回False
    :eg.
    whther_exist(dbh, repeat="a")
    """
    # if len(kwargs) == 0:
    #     return False

    result = dbh.find_one(kwargs)
    if result is None:
        return False
    else:
        return True


#像集合中插入某个键值
def insert_bad_url(collection, **kwargs):
    if whether_exist(collection, **kwargs) is False:
        collection.insert(kwargs, safe=True)

        # mongodbtest.insert_bad_url(collection, caipu_url=per_caipu_url[0])
        # dbh.error_download_caipu_url.insert({
        #     "caipu_url": per_caipu_url[0],
        # }, safe=True)

