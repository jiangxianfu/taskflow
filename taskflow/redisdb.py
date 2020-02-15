# -*- coding: utf-8 -*-

import redis
import settings
import json


class RedisDB:
    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __del__(self):
        self.close()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def push_msg_queue(self, instance_id):
        self.conn.lpush("taskflow:messagequeues", instance_id)

    def pop_msg_queue(self):
        return self.conn.rpop("taskflow:messagequeues")

    def add_running_instance(self, instance_id, dict_data):
        self.conn.hset("taskflow:activies", instance_id, json.dumps(dict_data))

    def remove_running_instance(self, instance_id):
        self.conn.hdel("taskflow:activies", instance_id)
