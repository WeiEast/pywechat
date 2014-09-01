#!/usr/bin/env python
#coding:utf-8


class JsOb:

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__.get(name, '')

    def __delattr__(self, name):
        if name in self.__dict__:
            del self.__dict__[name]

    def __str__(self):
        return self.__dict__.__str__()


if __name__ == '__main__':

    # a = JsOb(a=1, b=2)
    # a.name = 3
    # print(a)
    pass
