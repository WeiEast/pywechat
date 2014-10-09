#!/usr/bin/env python
#-*- coding:utf-8 -*-
# from _base.config import QINIU
from collections import defaultdict
import os
import json

# requirement:
# 1.下载qrsync同步工具 - > http://developer.qiniu.com/docs/v6/tools/qrsync.html
# 2.将此脚本与要上传的文件夹同级放置, 运行即可.


class QINIU:

    ACCESS_KEY = "VzrZ2ZjBIKyIImj6SwFU6TFCPIohtYC8PNCm5Oiy"
    SECRET_KEY = "8pJf3D5d8kzXLMh5kYkDaeAK-hiNi4Hr4HwdcHTQ&bucket=xwrwz&key_prefix=&threshold=333"
    BUCKET = "xwrwz"


def _html():
    html = defaultdict(list)
    for path, dirs, files in os.walk('.'):
        if path.startswith('./'):
            title = path.split('/')[1]
            for f in files:
                if f.startswith('.'):
                    continue
                if f.endswith('.jpg'):
                    html[title].append('../' + title + "/" + f)

    return html


def make_html():
    """将多个jpg文件转成html
    """
    TEMPLATE = """
    <!DOCTYPE html><meta charset="utf-8">
    <style>body{margin:0;padding:0;}img{margin:0;padding:0;width:100%%}</style>%s
    """
    if not os.path.exists('./html'):
        os.mkdir('./html')
    for k, v in _html().iteritems():
        with open('html/' + k + ".html", 'w') as h:
            h.write(TEMPLATE % "".join('<img src="' + str(i) + '">' for i in v))


def qrsync():
    """将HTML和对应的JPG上传到七牛.

    上传的HTML默认链接格式为: qiniu_host/html/html_name
    """
    CONFIG = {
        "src":          "./",
        "dest":         "qiniu:access_key={}&secret_key={}&bucket={}".format(QINIU.ACCESS_KEY, QINIU.SECRET_KEY, QINIU.BUCKET),
        "deletable":    0,
        "debug_level":  1
    }

    make_html()
    with open('./config', 'w') as f:
        f.write(json.dumps(CONFIG))
    os.system('qrsync config')


if __name__ == '__main__':
    qrsync()
