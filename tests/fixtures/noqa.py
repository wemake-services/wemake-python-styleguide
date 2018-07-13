# -*- coding: utf-8 -*-

"""
This file contains all possible errors.
"""

from .version import get_version  # noqa: Z100
def some():
    from my_module import some_function  # noqa: Z101


del {'a': 1}['a'] # noqa: Z102
raise  # noqa: Z103
raise NotImplemented  # noqa: Z104
hasattr(object, 'some')  # noqa: Z105
value = 1  # noqa: Z106
x = 2  # noqa: Z107
__private = 3  # noqa: Z108
__author__ = 'Nikita Sobolev'  # noqa: Z109

