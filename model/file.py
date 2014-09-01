#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
from collections import OrderedDict
from docutils import core
from _base.config import PATH


def folders_list(path):
    """列出给定path下的所有目录列表
    """
    _path = os.path.join(PATH.CONTENT_PATH, path)
    x = [x.encode('utf-8') for x in os.listdir(_path) if not x.startswith('.')]
    x.sort()

    return x


def files_list(path):
    """列出给定path下的所有文件名和内容. 返回一个{'file_name': 'file_connent'}字典
    """
    _path = os.path.join(PATH.CONTENT_PATH, path)
    data = OrderedDict()

    for file in os.listdir(_path):
        _content = open(os.path.join(_path, file)).read()
        if file.startswith('.'):
            continue
        if file.endswith('.rst'):
            content = reST_to_html_fragment(_content)
        else:
            content = _content

        data[file] = content
    data = OrderedDict(sorted(data.iteritems()))
    return data


def get_file_content(name, path=''):
    """ 获取文件内容
    """
    _path = os.path.join(PATH.CONTENT_PATH, path)
    for path, dirs, files in os.walk(_path):
        for each in files:
            if each == name:
                _content = open(os.path.join(path, name)).read()
                if name.endswith('.rst'):
                    content = reST_to_html_fragment(_content)
                else:
                    content = _content
                return content


def reST_to_html_fragment(a_str):
    parts = core.publish_parts(source=a_str, writer_name='html')

    return parts['body_pre_docinfo'] + parts['fragment']


def all_is_file(path):
        for f in os.listdir(path):
            if f.startswith('.'):
                continue
            if not f.endswith(('.txt', '.rst', '.pdf')):
                return False
        return True


if __name__ == '__main__':
    # print folders_list('tmp')
    # print get_file_content('__readme.txt', '办照指南/办照通用指南/5.其他常用指南')
    print files_list('办照指南/我去哪儿办照')
    pass
