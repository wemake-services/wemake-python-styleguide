# -*- coding: utf-8 -*-

"""
This fixture allows to check prohibited keywords.
"""

x = 0


def check_global():
    global x
    return


def check_nonlocal():
    nonlocal x
    return


def check_del():
    s = {'key': 'value'}
    del s['key']
    del s


def check_pass():
    pass
