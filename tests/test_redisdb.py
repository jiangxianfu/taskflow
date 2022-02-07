# -*- coding: utf-8 -*-
import unittest

from contrib.redisdb import RedisDB


class TestRedisDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db = RedisDB()

    def test_redisdb(self):
        self.db.conn.set("test_key", b"hello", ex=60)
        data = self.db.conn.get("test_key")
        assert b"hello" == data
