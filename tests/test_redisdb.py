# -*- coding: utf-8 -*-
import time
import unittest
from contrib.redisdb import RedisDB


class TestRedisDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db = RedisDB()

    def test_run_queue(self):
        instance = 1
        self.db.push_run_queue(instance)
        pop_value = self.db.pop_run_queue()
        assert int(pop_value) == instance

    def test_check_queue(self):
        instance = 1
        times = 1
        interval = 5
        self.db.set_check_queue(instance, times, interval)
        data = self.db.get_check_queue(instance)
        assert int(data) == times
        time.sleep(10)
        data = self.db.fetch_check_queue()
        assert len(data) > 0
        print('test check queue data:',type(data[0]), data[0])
        self.db.remove_check_queue(instance)
        self.db.del_check(instance)
