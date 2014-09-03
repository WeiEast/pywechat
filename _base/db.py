#!/usr/bin/env python
# coding:utf-8

from _base.config import REDIS
import redis as _redis
from _base.intstr import int_str
from _base.config import MONGO

# author: zsp

REDIS_KEY = 'RedisKey'
REDIS_KEY_ID = 'RedisKeyId'


_EXIST = set()


class RedisKey:

    def __init__(self, redis):
        self.redis = redis

    def __getattr__(self, attr):
        def _(name=''):
            return self(attr, name)
        return _

    def __call__(self, attr, name=''):
        key = attr + name
        redis = self.redis
        if key in _EXIST:
            raise Exception('redis key is already defined: %s' % key)
        _EXIST.add(key)
        if redis:
            _key = redis.hget(REDIS_KEY, key)
            if _key is None:
                _id = redis.incr(REDIS_KEY_ID)
                _key = int_str.encode(_id)
                if name and '%' in name:
                    _key = _key + "'" + name
                redis.hset(REDIS_KEY, key, _key)

            return _key


auth = "{}-{}-{}".format(REDIS.API_KEY, REDIS.SECRET_KEY, REDIS.NAME)
redis = _redis.StrictRedis(host="redis.duapp.com", port=80, password=auth)
# redis = _redis.StrictRedis(host="127.0.0.1", port=6379)
R = RedisKey(redis)
