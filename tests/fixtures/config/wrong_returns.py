# -*- coding: utf-8 -*-

"""
This file contains high functions with too many returns.
"""


def check_too_many_returns():
    if 1 == 2:
        return 1
    elif 1 == 3:
        return 2
    elif 1 == 4:
        return 3
    elif 1 == 5:
        return 4
    elif 1 == 6:
        return 5
    return 6  # error here


def acceptable_returns_count():
    if 1 == 2:
        return 1
    elif 1 == 3:
        return 2
    return 3


async def async_check_too_many_returns():
    if 1 == 2:
        return 1
    elif 1 == 3:
        return 2
    elif 1 == 4:
        return 3
    elif 1 == 5:
        return 4
    elif 1 == 6:
        return 5
    return 6  # error here


async def async_acceptable_returns_count():
    if 1 == 2:
        return 1
    elif 1 == 3:
        return 2
    return 3
