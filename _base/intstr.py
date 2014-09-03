#!/usr/bin/env python
#coding:utf-8
from string import ascii_letters


class IntStr:

    def __init__(self, alphabet, sign_character=None):
        self.alphabet = alphabet
        self.sign_character = sign_character
        self.base = len(alphabet)

    def encode(self, num):
        if num < 0:
            return self.sign_character + self.encode(-num)
        result = []
        while num:
            num, r = divmod(num, self.base)
            result.append(self.alphabet[r])

        return ''.join(reversed(result))

    def decode(self, s):
        if s.startswith(self.sign_character):
            return -self.decode(s[len(self.sign_character):])
        alphabet_index = {v: i for i, v in enumerate(self.alphabet)}
        n = 0
        for c in s:
            n = n * self.base + alphabet_index[c]
        return n

int_str = IntStr(ascii_letters)
