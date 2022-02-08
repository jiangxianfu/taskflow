# -*- coding: utf-8 -*-

import redis
from . import settings


class RedisDB(object):
    """
    Redis DB
    """

    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __del__(self):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def push_run_queue(self, instance_id):
        self.conn.lpush("taskflow:runqueue", instance_id)

    def set_check_hash(self, instance_id, times, interval):
        value = "%s,%s" %(times,interval)
        self.conn.hset("taskflow:checkhash", instance_id, value)

    def get_check_hash(self, instance_id) -> dict:
        value = self.conn.hget("taskflow:checkhash", instance_id)
        dict_data = None
        if value:
            arr = value.split(',')
            if len(arr)==2:
                dict_data["times"] = int(arr[0])
                dict_data["interval"] = int(arr[1])
        return dict_data
    def del_check_hash(self, instance_id):
        self.conn.hdel("taskflow:checkhash", instance_id)

    def get_all_check_hash(self):
        return self.conn.hgetall("taskflow:checkhash")

    def pop_run_queue(self):
        return self.conn.rpop("taskflow:runqueue")
