# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 数据库连接中心

"""
import pymysql


def connect_mysql(host, port, user, password, database):
    return pymysql.connect(host=host, port=port, user=user, password=password, database=database, ssl=None)


def connect_short(keyname):
    if keyname == "testdb":
        return connect_mysql("127.0.0.1", 3306, "test", "12345678", "testdb")
    return None
