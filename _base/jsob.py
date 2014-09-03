#!/usr/bin/env python
# coding:utf-8
from json import dumps


class JsOb(object):

    def __init__(self, *args, **kwds):
        for i in args:
            self.__dict__.update(args)
        self.__dict__.update(kwds)

    def __getattr__(self, name):
        return self.__dict__.get(name, '')

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            del self.__dict__['name']

    def __repr__(self):
        return self.__dict__.__repr__()

    __getitem__ = __getattr__
    __delitem__ = __delattr__
    __setitem__ = __setattr__

    def __len__(self):
        return self.__dict__.__len__()

    def __iter__(self):
        return self.__dict__.iteritems()

    def __contains__(self, name):
        return self.__dict__.__contains__(name)

    def __str__(self):
        return dumps(self.__dict__)


if __name__ == '__main__':

    # a = JsOb(a=1, b=2)
    # a.name = 3
    # print(a)
    pass
