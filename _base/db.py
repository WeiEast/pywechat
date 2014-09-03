#!/usr/bin/env python
# coding:utf-8

from _base.config import REDIS, MONGO
import redis as _redis
from _base.intstr import int_str
from mongokit import Document, Connection


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
R = RedisKey(redis)
# redis = _redis.StrictRedis(host="127.0.0.1", port=6379)


#### mongo
connection = Connection(host='mongo.duapp.com', port=8908)
# _db = connection[MONGO.NAME]
name = MONGO.name
connection.name.authenticate(MONGO.API_KEY, MONGO.SECRET_KEY)
mongo_db = connection.name


@connection.register
class UserResult(Document):
    __collection__ = 'user_result'
    __database__ = MONGO.NAME

    structure = dict(
        user_id=int,
        result=[]
    )
    default_values = {
        'result': [],
    }

# mongo_db = _db
