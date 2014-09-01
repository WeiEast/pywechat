#!/usr/bin/env python
# coding:utf-8
from functools import reduce
from _base.config import PATH
import os


def get_directory_structure(rootdir):
    """ 生成目录树形式的字典结构
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys([f for f in files if not f.startswith('.')])
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir

D = get_directory_structure(PATH.INDIVIDUAL_PATH)['个性化告知']
