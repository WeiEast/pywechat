#!/usr/bin/env python
# coding:utf-8
from _base.db import redis, R, mongo_db


R_USER_SELECT_LIST = R.USER_SELECT_LIST("%s")
R_USER_STATE_SET = R.USER_STATE_SET("%s")
# R_USER_RESULT_LIST = R.USER_RESULT_LIST("%s")


def user_select_new(id, select):
    redis.rpush(R_USER_SELECT_LIST % id, select)


def user_select_pop(id):
    redis.rpop(R_USER_SELECT_LIST % id)


def user_select_list(id, offset=0, limit=0):
    return redis.lrange(R_USER_SELECT_LIST % id, offset, offset + limit - 1)


def user_individuality_new(id):
    """用户请求了个性化告知服务
    """
    redis.sadd(R_USER_STATE_SET, id)


def user_in_indivduality(id):
    """用户是否在请求个性化告知状态
    """
    return redis.sismember(R_USER_STATE_SET, id)


def user_indivduality_rm(id):
    """退出个性化告知状态
    """
    redis.srem(R_USER_STATE_SET, id)


def user_rm(id):
    redis.delete(R_USER_SELECT_LIST % id)
    # redis.delete(R_USER_RESULT_LIST % id)
    user_result_rm(id)
    redis.srem(R_USER_STATE_SET, id)


def user_result_save(id, result):
    # redis.rpush(R_USER_RESULT_LIST % id, result)
    raise Exception(mongo_db.__dict__)
    u = mongo_db.UserResult.find_one(dict(user_id=id))
    if not u:
        u = mongo_db.UserResult()
    u['user_id'] = id
    u['result'].append(result)
    u.save()


def user_result_dumps(id):
    # return redis.lrange(R_USER_RESULT_LIST % id, offset, offset + limit - 1)
    result = mongo_db.UserResult.find_one(dict(user_id=id))
    return result['result'] if result else None


def user_result_rm(id):
    mongo_db.UserResult.collection.remove(dict(user_id=id))
