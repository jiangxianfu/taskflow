# -*- coding: utf-8 -*-
"""
test docker is ok
"""
import unittest

import redis
import pymysql
from pymysql.cursors import DictCursor
from contrib import settings


class TestDocker(unittest.TestCase):
    def test_database(self):
        mysqldb = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, user=settings.MYSQL_USER,
                                  password=settings.MYSQL_PWD, database=settings.MYSQL_DB, ssl=None,
                                  autocommit=True, cursorclass=DictCursor)
        mysqldb_cursor = mysqldb.cursor()
        mysqldb_cursor.execute("show tables;")
        data = mysqldb_cursor.fetchall()
        print('db tables:',data)
        self.assertTrue(data)

    def test_redis(self):
        redisdb = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redisdb.set("test_key", "123456", 60)
        data = redisdb.get("test_key")
        print('redis test_key data:',data)
        self.assertEqual(data, b"123456")
