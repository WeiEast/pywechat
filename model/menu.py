# -*- coding: utf-8 -*-
import requests
from _base.config import WECHAT
from yajl import loads, dumps

MENU_TEMPLE = {
    "button": [
        {
            "name": "办照指南",
            "sub_button": [
                {
                    "type": "click",
                    "name": "个性化告知",
                    "key": "personal_tell"
                },
                {
                    "type": "view",
                    "name": "我去哪儿办照",
                    "url": "http://pywechattest.duapp.com/guide/map"
                },
                {
                    "type": "view",
                    "name": "网上登记",
                    "url": "http://pywechattest.duapp.com/guide/web_register"
                },
                {
                    "type": "view",
                    "name": "三证合一办理",
                    "url": "http://pywechattest.duapp.com/guide/3in1"
                },
                {
                    "type": "view",
                    "name": "办照通用指南",
                    "url": "http://pywechattest.duapp.com/guide/licence"
                },
            ]
        },
        {
            "name": "信用查询",
            "sub_button": [
                {
                    "type": "view",
                    "name": "信用查询平台",
                    "url": "http://qyxy.baic.gov.cn/"
                },
                {
                    "type": "view",
                    "name": "信用信息APP",
                    "url": "http://pywechattest.duapp.com/truth/app"
                },
                {
                    "type": "view",
                    "name": "信用信息查询",
                    "url": "http://qyxy.baic.gov.cn/"
                }
            ]
        },
        {
            "name": "工商e典",
            "sub_button": [
                {
                    "type": "view",
                    "name": "微服务",
                    "url": "http://pywechattest.duapp.com/e/server"
                },
                {
                    "type": "view",
                    "name": "微互动",
                    "url": "http://pywechattest.duapp.com/e/interactive"
                },
                {
                    "type": "view",
                    "name": "微导航",
                    "url": "http://pywechattest.duapp.com/e/map"
                }
            ]
        }
    ]
}


def create_menu():

    _url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
    _rp = requests.get(_url.format(WECHAT.APPID, WECHAT.APPSECRET))
    access_token = loads(_rp.text)['access_token']

    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}".format(access_token)
    response = requests.post(url, data=dumps(MENU_TEMPLE))

    return loads(response.text)['errmsg']


if __name__ == '__main__':
    status = create_menu()
    print(status)
