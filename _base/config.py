#!/usr/bin/env python
#coding:utf-8


class WECHAT:
    APPID = "wx5c410437a8e81c6f"
    APPSECRET = "64b6cc4ab4bb33e38979105d52344b39"
    TOKEN = "helloworld"
    INDIVIDUAL_TOKEN = 'personal_tell'


class REDIS_CONFIG:

    NAME = "LQqdnxqpggsdMJUiidei"
    API_KEY = "GQdqg6hNadUr8uWztdezqQqA"
    SECRET_KEY = "bdHVnQkuovvaOpo6idKQ5m5j5vGEbnkP"


class HOST:

    MAIN = "http://pywechattest.duapp.com"
    QINIU = "http://xwrwz.qiniudn.com/html/"


class PATH:
    from os.path import abspath, dirname, join
    _prefix = abspath(join(dirname(abspath(__file__)), '../'))

    INDIVIDUAL_PATH = _prefix + "/content/办照指南/个性化告知"  # 存放个性化告知的目录
    CONTENT_PATH = _prefix + '/content'  # 存放所有文件内容的目录


class QINIU:

    ACCESS_KEY = "VzrZ2ZjBIKyIImj6SwFU6TFCPIohtYC8PNCm5Oiy"
    SECRET_KEY = "8pJf3D5d8kzXLMh5kYkDaeAK-hiNi4Hr4HwdcHTQ&bucket=xwrwz&key_prefix=&threshold=333"
    BUCKET = "xwrwz"
