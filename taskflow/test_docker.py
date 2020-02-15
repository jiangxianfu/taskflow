# -*- coding: utf-8 -*-

import redis
import pymysql
import settings

mysqldb = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, user=settings.MYSQL_USER,
                password=settings.MYSQL_PWD, database=settings.MYSQL_DB, ssl=None)
mysqldb_cursor = mysqldb.cursor()
mysqldb_cursor.execute("show tables;")
data = mysqldb_cursor.fetchall()
print(data)

redisdb = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

redisdb.set("test_key","123456",60)
data = redisdb.get("test_key")
print(data)