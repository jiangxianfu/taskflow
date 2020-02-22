# -*- coding: utf-8 -*-
import settings
import redis

print(settings.REDIS_HOST)
db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def test_redisdb():
    db.set("test_key", b"hello", ex=60)
    data = db.get("test_key")
    assert b"hello" == data
