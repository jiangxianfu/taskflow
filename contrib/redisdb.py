# -*- coding: utf-8 -*-

import redis
from . import settings
import time


class RedisDB(object):
    """
    Redis DB
    """

    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                                encoding="utf-8", decode_responses=True)

    def __del__(self):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def pop_run_queue(self):
        return self.conn.rpop("taskflow:runqueue")

    def push_run_queue(self, instance_id):
        self.conn.lpush("taskflow:runqueue", instance_id)

    def set_check_queue(self, instance_id, times, interval):
        next_time = int(time.time()) + int(interval)
        self.conn.set("taskflow:check:instances:%s" % instance_id, times)
        self.conn.zadd("taskflow:check:sorted_set", {str(instance_id): next_time, })

    def get_check_queue(self, instance_id):
        times = self.conn.get("taskflow:check:instances:%s" % instance_id)
        return int(times) if times else 0

    def del_check(self, instance_id):
        self.conn.zrem("taskflow:check:sorted_set", str(instance_id))
        self.conn.delete("taskflow:check:instances:%s" % instance_id)
    
    def remove_check_queue(self, instance_id):
        self.conn.zrem("taskflow:check:sorted_set", str(instance_id))

    def fetch_check_queue(self, limit=50):
        cur_time = int(time.time())
        return self.conn.zrangebyscore("taskflow:check:sorted_set", min=0, max=cur_time, start=0, num=limit)
