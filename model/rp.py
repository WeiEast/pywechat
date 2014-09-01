# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


########## 预定义回复  ##########

RP = {}
# article_url = "http://pwechat.duapp.com/weixin/article?name={}"
# picture text
# formation: {type, title, content, pic_url, url}
# RULES['pic'] = [1, "Help Info", "我真的是一个图文信息:)",
#                 "http://kzing.net/static/Image/homePagePic.jpg",
#                 article_url.format("help.md")]

# RULES['tp'] = [1, "hello, pic", "我也是图文信息",
#                "http://www.baidu.com/img/baidu_sylogo1.gif", article_url.format('nothing')]


# normal text
# formation: {type, content}
# RULES['code'] = [0, "I Love coding :)"]
# RULES['chinese'] = [0, "你好, 需求是什么? :)"]
# RULES['help'] = [0, "帮助信息:\n回复pic, 查看图文信息\n回复chinese,查看中文信息\n... ..."]
