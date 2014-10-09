#!/usr/bin/env python
# coding:utf-8

from config import REDIS
import redis as _redis
from intstr import int_str


REDIS_KEY = 'RedisKey'
REDIS_KEY_ID = 'RedisKeyId'


_EXIST = set()


class RedisKey:

    def __init__(self, redis):
        self.redis = redis

    def __getattr__(self, attr):
        return lambda name='': self(attr, name)

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
