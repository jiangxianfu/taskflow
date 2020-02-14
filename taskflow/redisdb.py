# -*- coding: utf-8 -*-

import redis
import settings
import json


class RedisDB:
    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __del__(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def push_msg_queue(self, instance_id):
        self.conn.lpush("taskflow:messagequeues", instance_id)

    def pop_msg_queue(self):
        return self.conn.rpop("taskflow:messagequeues")

    def set_running_instance(self, key, value):
        self.conn.set(key, json.dumps(value), ex=1 * 24 * 60 * 60)
