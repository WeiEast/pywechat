#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 被抛弃的需求, 但它是能用的 --- 在解除一些注释后.: )
# 预定义回复: 接受用户发来的消息, 返回定义好的内容. 如: "现在几点?" -> "25:00pm"
RP = {}

text = 0
pic = 1


# 文本回复
# 格式: [关键词] = [类型, 内容]
# 示例: RP[some_key_word] = [text, "I Love Coding"]


# 图文回复
# 格式: [关键词] = [类型, 标题, 内容, 图片链接, 文章链接]
# 示例: RP[some_key_word] = [pic, "title", 'content', "image_url", "article_url"]
