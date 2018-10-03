# -*- coding: utf-8 -*-

"""
This file contains stuff that has too many expressions.
"""

def check_expressions_in_function():
    1 / 0
    print(1)
    x
    1 / 0
    print(1)
    x
    1 / 0
    print(1)
    x

    1 / x  # error here


async def async_check_expressions_in_function():
    1 / 0
    print(1)
    x
    1 / 0
    print(1)
    x
    1 / 0
    print(1)
    x

    1 / x  # error here
