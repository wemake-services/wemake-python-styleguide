# -*- coding: utf-8 -*-

"""
This file contains all possible violations.
"""

from __future__ import print_function  # noqa: Z422

from .version import get_version  # noqa: Z300

full_name = u'Nikita Sobolev'  # noqa: Z302
phone_number = 555_123_999  # noqa:  Z303
partial_number = .05  # noqa: Z304
formatted_string = f'Hi, {full_name}'  # noqa: Z305


def some():  # noqa: Z110, Z113
    from my_module import some_function  # noqa: Z435

    class Nested(object): ...  # noqa: 431

    def nested(): ...  # noqa: Z430


del {'a': 1}['a'] # noqa: Z420
raise NotImplemented  # noqa: Z423
hasattr(object, 'some')  # noqa: Z421
value = 1  # noqa: Z110
x = 2  # noqa: Z111
__private = 3  # noqa: Z112
__author__ = 'Nikita Sobolev'  # noqa: Z410

nodes = [node for node in 'abc' if node != 'a' if node != 'b']  # noqa: Z307


class BadClass:  # noqa: Z306
    @staticmethod  # noqa: Z433
    def some_static():
        ...

    @staticmethod  # noqa: Z433
    async def some_async_static():
        ...

    def __del__(self, *args, **kwargs):  # noqa: Z434
        ...

    class Nested:  # noqa: Z306,Z431
        ...


magic_numbers = 13.2 + 50  # noqa: Z432

hex_number = 0XFF  # noqa: Z309
octal_number = 0O11  # noqa: Z309
binary_number = 0B1001  # noqa: Z309
number_with_scientific_notation = 1.5E+10  # noqa: Z309
