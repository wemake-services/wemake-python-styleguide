# -*- coding: utf-8 -*-

"""
This file contains all broken variable names.
"""

x = 1  # one letter variables are prohibited


def check_function_args(data, t):
    result = data + t
    return result


with open('missing.txt') as f:
    contents = f.read()  # the same as `content`, prohibited
    print(contents)


for item in range(1, 3):
    continue


class Fixture(object):
    data = 'data'
    result: int

    def __init__(self, value):
        self.var = value  # error here only for `var`, not for `value`


val = Fixture()  # val is forbidden
print(val.var)  # no error here
