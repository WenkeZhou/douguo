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
# def whether_exist(collection):
#     result = dbh.test.find({key:value}).count()





