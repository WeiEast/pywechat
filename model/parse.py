#!/usr/bin/env python
# coding:utf-8
import hashlib
from _base.config import WECHAT
import xml.etree.ElementTree as ET


def verify(request):
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    _t = ''.join(sorted([WECHAT.TOKEN, timestamp, nonce]))
    hashstr = hashlib.sha1(_t).hexdigest()

    return hashstr == signature


def parse_msg(msg):
    return {c.tag: c.text for c in ET.fromstring(msg)}


def is_text_msg(msg):
    return msg['MsgType'] == 'text'


def is_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'


def is_click_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'CLICK'
