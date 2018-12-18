# -*- coding: utf-8 -*-

"""
This file contains all possible violations.

It is used for e2e tests.
"""

from __future__ import print_function  # noqa: Z422

import os.path  # noqa: Z301
import sys as sys  # noqa: Z113

from some import _protected  # noqa: Z440

from .version import get_version  # noqa: Z300

full_name = u'Nikita Sobolev'  # noqa: Z302
phone_number = 555_123_999  # noqa:  Z303
partial_number = .05  # noqa: Z304
formatted_string = f'Hi, {full_name}'  # noqa: Z305


def function_name(
    value: int = 0,  # noqa: Z110
):
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/392
    anti_z444 = 1


def some():  # noqa: Z110
    from my_module import some_function  # noqa: Z435

    class Nested(object):  # noqa: Z431
        ...  # noqa: Z444

    def nested():  # noqa: Z430
        anti_z444 = 1

    raise NotImplemented  # noqa: Z423


del {'a': 1}['a'] # noqa: Z420
hasattr(object, 'some')  # noqa: Z421
value = 1  # noqa: Z110
x = 2  # noqa: Z111
__private = 3  # noqa: Z112
star_wars_episode_7 = 'the worst episode ever'  # noqa: Z114
consecutive__underscores = 4  # noqa: Z116
cls = 5  # noqa: Z117
__author__ = 'Nikita Sobolev'  # noqa: Z410
extremely_long_name_that_needs_to_be_shortened_to_work_fine = 2  # noqa: Z118
привет_по_русски = 'Hello, world!'  # noqa: Z119

some._execute()  # noqa: Z441


def many_locals():  # noqa: Z210
    arg1, arg2, arg3, arg4, arg5, arg6 = range(6)


def many_arguments(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6):  # noqa: Z211
    anti_z444 = 1


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
    anti_z444 = 1


def test_function():
    if xy > 1:
        if xy > 2:
            if xy > 3:
                if xy > 4:
                    if xy > 5:
                        test(5)  # noqa: Z220


line = some.call(7 * 2, 3 / 4) / some.run(5 / some, 8 - 2 + 1)  # noqa: Z221
if line and line > 2 and line > 3 and line > 4 and line > 5:  # noqa: Z221,Z222
    anti_z444 = 1

if line:  # noqa: Z223
    anti_z444 = 1
elif line > 1:
    anti_z444 = 1
elif line > 2:
    anti_z444 = 1
elif line > 3:
    anti_z444 = 1
elif line > 4:
    anti_z444 = 1


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
        anti_z444 = 1

    @staticmethod  # noqa: Z433
    async def some_async_static():
        anti_z444 = 1

    def __del__(self, *_args, **_kwargs):  # noqa: Z434
        anti_z444 = 1

    class Nested:  # noqa: Z306,Z431
        anti_z444 = 1


magic_numbers = 13.2 + 50  # noqa: Z432

nodes = [node for node in 'abc' if node != 'a' if node != 'b']  # noqa: Z307

assert 1 > 1 > hex_number  # noqa: Z308
assert 2 > octal_number  # noqa: Z309

hex_number = 0XFF  # noqa: Z310
octal_number = 0O11  # noqa: Z310
binary_number = 0B1001  # noqa: Z310
number_with_scientific_notation = 1.5E+10  # noqa: Z310

if '6' in nodes in '6':  # noqa: Z311
    anti_z444 = 1

assert hex_number == hex_number  # noqa: Z312


async def test_function():
    return(123, 33)  # noqa: Z313


if True:  # noqa: Z314
    anti_z444 = 1


class SomeClass(FirstParent, SecondParent, object):  # noqa: Z315
    anti_z444 = 1


class SomeClass(FirstParent,  # noqa: Z317
                SecondParent,  # noqa: Z318
                ThirdParent):  # noqa: Z319
    anti_z444 = 1


if SomeClass:
        print(SomeClass)  # noqa: Z318

some_set = {1
           }  # noqa: Z318

print(
    1,
    2)  # noqa: Z319


def function(  # noqa: Z320
    arg: Optional[  # noqa: Z320
        str,
    ]
) -> Optional[
    str,
]:
    anti_z444 = 1


string_modifier = R'(s)'  # noqa: Z321

try:
    anti_z444 = 1
except BaseException:  # noqa: Z424
    anti_z444 = 1

call_with_positional_bool(True)  # noqa: Z425

for symbol in 'abc':  # noqa: Z436
    anti_z444 = 1
else:
    anti_z444 = 1


try:  # noqa: Z437
    anti_z444 = 1
finally:
    anti_z444 = 1

nodes = nodes  # noqa: Z438


class Example(object):
    """Correct class docstring."""

    def __init__(self):  # noqa: Z439
        """Correct function docstring."""
        yield 10


for index in range(6):  # noqa: Z442
    print(lambda: index)


async def function_with_unreachable():
    await test_function()
    raise ValueError()
    print(1)  # noqa: Z443


1 + 2  # noqa: Z444

first = second = 2  # noqa: Z445


try:  # noqa: Z446
    anti_z444 = 1
except ValueError:
    anti_z444 = 1
except ValueError:
    anti_z444 = 1
