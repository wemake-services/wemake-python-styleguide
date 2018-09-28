# -*- coding: utf-8 -*-

"""
This file contains all possible errors.
"""

from __future__ import print_function  # noqa: Z102

from .version import get_version  # noqa: Z100

full_name = u'Nikita Sobolev'  # noqa: Z001
phone_number = 555_123_999  # noqa: Z002
partial_number = .05  # noqa: Z004


def some():  # noqa: Z113
    from my_module import some_function  # noqa: Z101

    def nested(): ...  # noqa: Z200


del {'a': 1}['a'] # noqa: Z110
raise NotImplemented  # noqa: Z111
hasattr(object, 'some')  # noqa: Z112
value = 1  # noqa: Z113
x = 2  # noqa: Z114
__private = 3  # noqa: Z115
__author__ = 'Nikita Sobolev'  # noqa: Z116

nodes = [node for node in 'abc' if node != 'a' if node != 'b']  # noqa: Z120

class BadClass:  # noqa: Z302
    @staticmethod  # noqa: Z300
    def some_static():
        ...

    def __del__(self, *args, **kwargs):  # noqa: Z301
        ...

    class Nested:  # noqa: Z201,Z302
        ...

magic_numbers = 13.2 + 50  # noqa: 214
