# -*- coding: utf-8 -*-

"""
This file contains all broken variable names.
"""

x = 1  # error here


def check_function_args(data, t, *a, **vals):  # 4 errors here
    result = data + t  # error here for `result`
    return result


with open('missing.txt') as f:  # error here
    contents = f.read()  # error here
    print(contents)


for item in range(1, 3):  # error here
    continue


for _ in range(1, 3):  # should not raise error here
    continue


try:
    1 / 0
except ZeroDivisionError as e:  # TODO: error here
    pass


class Fixture(object):
    data = 'data'  # error here
    result: int  # error here

    def __init__(self, value):  # error here
        self.var = value  # error here only for `var`, not for `value`


val = Fixture()  # error here
print(val.var)  # no error here
