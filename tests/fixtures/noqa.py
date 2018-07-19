# -*- coding: utf-8 -*-

"""
This file contains all possible errors.
"""

from __future__ import print_function  # noqa: Z102
from .version import get_version  # noqa: Z100
def some():
    from my_module import some_function  # noqa: Z101


del {'a': 1}['a'] # noqa: Z110
raise  # noqa: Z111
raise NotImplemented  # noqa: Z112
hasattr(object, 'some')  # noqa: Z113
value = 1  # noqa: Z114
x = 2  # noqa: Z115
__private = 3  # noqa: Z116
__author__ = 'Nikita Sobolev'  # noqa: Z117


class BadClass:  # noqa: Z302
    @staticmethod  # noqa: Z300
    def some_static(): ...

    def __del__(self, *args, **kwargs): ...  # noqa: Z301
