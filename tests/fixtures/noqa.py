"""
This file contains all possible violations.

It is used for e2e tests.
"""

from __future__ import print_function  # noqa: Z422

from .version import get_version  # noqa: Z300
import os.path  # noqa: Z301
import sys as sys  # noqa: Z113
from some import _protected  # noqa: Z440

full_name = u'Nikita Sobolev'  # noqa: Z302
phone_number = 555_123_999  # noqa:  Z303
partial_number = .05  # noqa: Z304
formatted_string = f'Hi, {full_name}'  # noqa: Z305


def some():  # noqa: Z110
    from my_module import some_function  # noqa: Z435

    class Nested(object): ...  # noqa: Z220, Z431

    def nested(): ...  # noqa: Z430


del {'a': 1}['a'] # noqa: Z420
raise NotImplemented  # noqa: Z423
hasattr(object, 'some')  # noqa: Z421
value = 1  # noqa: Z110
x = 2  # noqa: Z111
__private = 3  # noqa: Z112
star_wars_episode_7 = 'the worst episode ever'  # noqa: Z114
consecutive__underscores = 4  # noqa: Z116
cls = 5  # noqa: Z117
переменная = 42  # noqa: Z118
__author__ = 'Nikita Sobolev'  # noqa: Z410

some._execute()  # noqa: Z441


def many_locals():  # noqa: Z210
    arg1, arg2, arg3, arg4, arg5, arg6 = range(6)


def many_arguments(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6):  # noqa: Z211
    ...


def many_returns(xy):  # noqa: Z212
    if xy > 1:
        return 1
    if xy > 2:
        return 2
    if xy > 3:
        return 3
    if xy > 4:
        return 4
    if xy > 5:
        return 5
    return 6


def many_expressions(xy):  # noqa: Z213
    print(xy)
    print(xy)
    print(xy)

    print(xy)
    print(xy)
    print(xy)

    print(xy)
    print(xy)
    print(xy)

    print(xy)


class ManyParents(dict, list, tuple, Exception):  # noqa: Z215
    ...


line = some.call(7 * 2, 3 / 4) / some.run(5 / some, 8 - 2 + 1)  # noqa: Z221
if line and line > 2 and line > 3 and line > 4 and line > 5:  # noqa: Z221,Z222
    ...

if line:  # noqa: Z223
    ...
elif line > 1:
    ...
elif line > 2:
    ...
elif line > 3:
    ...
elif line > 4:
    ...


numbers = [
    target  # noqa: Z224
    for assignment in range(hex_number)
    for target in range(assignment)
    for _ in range(10)
    if isinstance(target, int)
]


class BadClass:  # noqa: Z306
    UPPER_CASE_ATTRIBUTE = 12  # noqa: Z115

    @staticmethod  # noqa: Z433
    def some_static():
        ...

    @staticmethod  # noqa: Z433
    async def some_async_static():
        ...

    def __del__(self, *_args, **_kwargs):  # noqa: Z434
        ...

    class Nested:  # noqa: Z306,Z431
        ...


magic_numbers = 13.2 + 50  # noqa: Z432

nodes = [node for node in 'abc' if node != 'a' if node != 'b']  # noqa: Z307

assert 1 > 1 > hex_number  # noqa: Z308
assert 2 > octal_number  # noqa: Z309

hex_number = 0XFF  # noqa: Z310
octal_number = 0O11  # noqa: Z310
binary_number = 0B1001  # noqa: Z310
number_with_scientific_notation = 1.5E+10  # noqa: Z310

if '6' in nodes in '6':  # noqa: Z311
    ...

assert hex_number == hex_number  # noqa: Z312


def test_function():
    return(123, 33)  # noqa: Z313


if True:  # noqa: Z314
    ...


class SomeClass(FirstParent, SecondParent, object):  # noqa: Z315
    ...


try:
    ...
except BaseException:  # noqa: Z424
    ...

for symbol in 'abc':  # noqa: Z436
    ...
else:
    ...


try:  # noqa: Z437
    ...
finally:
    ...

nodes = nodes  # noqa: Z438


class Example(object):
    def __init__(self):  # noqa: Z439
        yield 10


for index in range(6):  # noqa: Z442
    print(lambda: index)
