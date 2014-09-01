#!/usr/bin/env python
# coding:utf-8

from templates import TEMPLATE_TEXT, NEWS_MSG_HEADER_TPL, NEWS_MSG_ITEM_TPL, NEWS_MSG_TAIL
from const import FIND_NO_RP, NO_THIS_SELECTION, ANSWER_LINK, EXTRA_NOTICE
from rp import RP
from user import user_select_new, user_select_list, user_select_pop, user_result_save, user_rm, user_result_dumps
from time import time
import re
import os
from decision import decision_links_dumps
from _base.config import GLOBAL
from file import reST_to_html_fragment, all_is_file


BACK_TO_LAST = '0'        # 返回上层
MULTI_FLAG = ','          # 多选标志


class Responser:

    """预定义回复: 回复在rp.py预定义的内容, 包括普通文本信息和图文信息两种格式.
    """

    NORMAL_TXT = 0
    PIC_TXT = 1

    def __init__(self, msg):
        self.msg = msg

    def make_rp(self):

        data = self.msg['Content']
        rp = self.find_rp(data)
        if rp:
            type = rp[0]
            if type == self.NORMAL_TXT:
                return self.rp_text_msg(rp[1])
            elif type == self.PIC_TXT:
                return self.rp_pic_msg([Item(rp[1], rp[2], rp[3], rp[4])])

        else:
            return self.rp_text_msg(FIND_NO_RP)

    def find_rp(self, rule):

        return RP.get(rule, '')

    def rp_text_msg(self, content):

        return TEMPLATE_TEXT % (self.msg['FromUserName'], self.msg['ToUserName'],
                                str(int(time())), content)

    def rp_pic_msg(self, content):

        msg_header = NEWS_MSG_HEADER_TPL % (self.msg['FromUserName'], self.msg['ToUserName'],
                                            str(int(time())), len(content))

        _ = lambda item: NEWS_MSG_ITEM_TPL % (item.title, item.description, item.picUrl, item.url)
        rp = ''.join(_(x) for x in content)

        return '{}{}{}'.format(msg_header, rp, NEWS_MSG_TAIL)


class IndividualRepoter:

    """个性化回复: 根据用户选择和给定文件夹下的内容生成不同的回复.
    """

    SELECT_FAIL = 0           # 错误的选择
    IS_ANSWER = 1             # 问答结束
    M_CONTINUE_ASK = 2        # 多选: 需要继续提问
    M_IS_ANSWER = 3           # 多选: 直接返回答案

    # @param msg: 从微信获取的用户信息
    # @param D: 保存着目录结构的字典
    # @root: 存放个性化回复的根目录
    def __init__(self, msg, D, root):
        self.msg = msg
        self.D = D
        self.root = root
        self.path = []
        self.id = self.msg['FromUserName']
        self._files = set()  # 用于剔除重复文件

    def individual_response(self):
        new = self.msg['Content']
        user_select = user_select_list(self.id)
        result = ''

        if new == BACK_TO_LAST:  # 返回上层
            if user_select:
                user_select.pop()
                user_select_pop(self.id)
        else:
            user_select.append(new)
            user_select_new(self.id, new)

        rp = self.find_individual_rp(user_select)

        if rp == self.SELECT_FAIL:
            result = NO_THIS_SELECTION
        elif rp == self.IS_ANSWER:
            result = ANSWER_LINK.format(GLOBAL.HOST, 'individual', self.id)
        else:
            result = '{}{}'.format(rp, EXTRA_NOTICE)

        return result

    def find_individual_rp(self, select_list):
        """基于D字典结构实现
        规则: 文件夹作为'问题'返回, 普通文件(除 readme.txt 外)作为'答案'储存在 redis 中,返回一个链接.
        """
        assert select_list != [], "select list shouldn't be empty"
        multi_state = ''
        try:
            for s in select_list:
                if s.find(MULTI_FLAG) != -1:
                    if s == select_list[-1]:  # 普通多选
                        multi_state = self.multi_select(s)
                    elif s == select_list[-2]:  # 生成上一次多选的结果
                        multi_state = self.multi_select(s, special=select_list[-1])
                        break
                    else:
                        raise SelectException('Multi select fail')
                else:
                    self.single_select(s)

        except SelectException:
            return self.SELECT_FAIL

        else:
            if multi_state == self.M_IS_ANSWER:
                return self.IS_ANSWER
            else:
                files = sorted(self.D.keys(), key=self._key)
                path = self.root + '/' + os.sep.join(self.path)

                readme, content, continue_ask = self.get_files_content(files, path)
                result = '\n'.join([readme, content])

                if continue_ask:
                    return result.strip()
                else:
                    result += decision_links_dumps(user_select_list(self.id), MULTI_FLAG)  # 可能需要股东决议书等
                    user_result_save(self.id, result.strip())
                    return self.IS_ANSWER

    def multi_select(self, select, special=None):
        multi_select = select.split(MULTI_FLAG)
        path = self.root + '/' + os.sep.join(self.path)
        next_key = ''
        result = ''

        keys = self.key_complete(multi_select)
        if not keys:
            raise SelectException('Unavailable selects: {}'.format(select))

        for k in keys:
            file_path = os.path.join(path, k)

            if all_is_file(file_path):
                files = sorted(self.D[k].keys(), key=self._key)
                result += '\n' + self.get_files_content(files, file_path)[1]
            elif special:
                _key = self.key_complete([special], _next=k)[0]
                files = sorted(self.D[k][_key].keys(), key=self._key)
                result += '\n' + self.get_files_content(files, os.path.join(file_path, _key))[1]

            elif not special and not next_key:
                next_key = k

        if next_key:
            self.path.append(next_key)
            self.D = self.D[next_key]

        if result:
            if next_key:
                user_result_save(self.id, result.strip())
                return self.M_CONTINUE_ASK
            else:
                result += decision_links_dumps(user_select_list(self.id), MULTI_FLAG)  # 可能需要股东决议书
                user_result_save(self.id, result.strip())
                return self.M_IS_ANSWER

    def single_select(self, s):
        key = self.key_complete([s])
        if key:
            self.path.append(key[0])
            self.D = self.D[key[0]]
        else:
            raise SelectException('Unavailable select: {}'.format(s))

    def key_complete(self, select, _next=None):

        keys = []
        _D = self.D if not _next else self.D[_next]
        for s in select:
            for key in _D:
                search = re.search(r'\d+', key)
                if search and s == search.group():
                    keys.append(key)
                    break
            else:
                return ''
        return keys

    def get_files_content(self, files, path):
        readme = content = ''
        continue_ask = True
        for file in files:
            if file in self._files:
                continue  # 内容已经读取过
            abs_path = os.path.join(path, file)
            if file.endswith(('.rst', '.txt')):
                if file == 'readme.txt':
                    readme = open(abs_path).read()
                else:
                    if file.endswith('.rst'):
                        _content = reST_to_html_fragment(open(abs_path).read())
                    else:
                        _content = open(abs_path).read()

                    content += '<div class="header">{}</div>'.format(_content)
                    self._files.add(file)
                    continue_ask = False
            elif continue_ask and os.path.isdir(abs_path):
                content += '\n' + file

        return readme, content, continue_ask

    def _key(self, s):
        r = re.search('\d+', s)
        return int(r.group()) if r else -1


class SelectException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Item:

    def __init__(self, title, txt, pic_url, url):
        self.title = title
        self.txt = txt
        self.pic_url = pic_url
        self.url = url


if __name__ == '__main__':

    # from directory_tree import D
    # msg = {'FromUserName': 'lzy', 'ToUserName': 'kzing'}

    # select = ['2', '1', '1,5,6,7,8', '3']
    # user_rm('lzy')
    # for i in select:
    #     msg['Content'] = i
    #     r = IndividualRepoter(msg, D, PATH.INDIVIDUAL_PATH)
    #     r.individual_response()
        # print user_select_list(msg['FromUserName'])
    # print D
    # print(user_result_dumps(msg['FromUserName']))
    pass
