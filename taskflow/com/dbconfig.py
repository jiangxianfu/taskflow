# -*- coding: utf-8 -*-
"""
author: jiangxf
date: 2020-01-29
description: 该方法主要是用于启动整个工作流程序

"""
import pymysql


def __conn_mysql(host, port, user, password, database):
    return pymysql.connect(host=host, port=port, user=user, password=password, database=database, ssl=None)


def connect_short(keyname):
    if keyname == "testdb":
        return __conn_mysql("127.0.0.1", 3306, "test", "12345678", "testdb")
    raise ("not exits keyname")
