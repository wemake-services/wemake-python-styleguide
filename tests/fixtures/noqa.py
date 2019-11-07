# -*- coding: utf-8 -*-

"""
This file contains all possible violations.

It is used for e2e tests.
"""

from __future__ import print_function  # noqa: WPS422

import os.path  # noqa: WPS301
import sys as sys  # noqa: WPS113

from some import _protected  # noqa: WPS436

from .version import get_version  # noqa: WPS300

full_name = u'Nikita Sobolev'  # noqa: WPS302
phone_number = 555_123_999  # noqa:  WPS303
partial_number = .05  # noqa: WPS304
formatted_string = f'Hi, {full_name}'  # noqa: WPS305


def __getattr__():  # noqa: WPS413
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/461
    anti_z444 = 1


def foo_func():
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/601

    yield (1, 2, 3, 4, 5, 6)  # noqa: WPS227


print(x > 2 > y > 4)  # noqa: WPS228

try:  # noqa: WPS229
    print(1)
    print(2)
    print(3)
except AnyError:
    print('nope')


class TooManyPublicAtts(object):  # noqa: WPS230
    def __init__(self):
        self.first = 1
        self.second = 2
        self.third = 3
        self.fourth = 4
        self.fifth = 5
        self.sixth = 6
        self.boom = 7


def function_name(
    value: int = 0,  # noqa: WPS110
):
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/392
    anti_z444 = 1


def some():  # noqa: WPS110
    from my_module import some_import  # noqa: WPS433

    class Nested(object):  # noqa: WPS431
        ...  # noqa: WPS428, WPS604

    def nested():  # noqa: WPS430
        anti_z444 = 1

    raise NotImplemented  # noqa: WPS423


del {'a': 1}['a']  # noqa: WPS420
hasattr(object, 'some')  # noqa: WPS421
value = 1  # noqa: WPS110
x = 2  # noqa: WPS111
__private = 3  # noqa: WPS112
star_wars_episode_7 = 'the worst episode ever after 8'  # noqa: WPS114
consecutive__underscores = 4  # noqa: WPS116
cls = 5  # noqa: WPS117
__author__ = 'Nikita Sobolev'  # noqa: WPS410
extremely_long_name_that_needs_to_be_shortened_to_work_fine = 2  # noqa: WPS118
привет_по_русски = 'Hello, world!'  # noqa: WPS119
wrong_alias_ = 'some fake builtin alias'  # noqa: WPS120

def some_function():
    _should_not_be_used = 1  # noqa: WPS122
    print(_should_not_be_used)  # noqa: WPS121

used, __ = 1, 2  # noqa: WPS123

some._execute()  # noqa: WPS437


def many_locals():  # noqa: WPS210
    arg1, arg2, arg3, arg4, arg5, arg6 = range(6)


def many_arguments(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6):  # noqa: WPS211
    anti_z444 = 1


def many_returns(xy):  # noqa: WPS212
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


def many_expressions(xy):  # noqa: WPS213
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


class ManyParents(First, Second, Third, Exception):  # noqa: WPS215
    anti_z444 = 1


async def too_many_awaits():  # noqa: WPS217
    await test_function(1)
    await test_function(2)
    await test_function(3)
    await test_function(4)
    await test_function(5)
    await test_function(6)
    await test_function(7)


async def too_many_asserts():  # noqa: WPS218
    assert test_function(1)
    assert test_function(2)
    assert test_function(3)
    assert test_function(4)
    assert test_function(5)
    assert test_function(6)

deep_access = some.other[0].field.type.boom  # noqa: WPS219

def test_function():  # noqa: WPS231
    if xy > 1:
        if xy > 2:
            if xy > 3:
                if xy > 4:
                    if xy > 5:
                        test(5)  # noqa: WPS220


line = some.call(7 * 2, 3 / 4) / some.run(5 / some, 8 - 2 + 6)  # noqa: WPS221
if line and line > 2 and line > 3 and line > 4 and line > 5:  # noqa: WPS221,WPS222
    anti_z444 = 1

if line:  # noqa: WPS223
    anti_z444 = 1
elif line > 1:
    anti_z444 = 1
elif line > 2:
    anti_z444 = 1
elif line > 3:
    anti_z444 = 1
elif line > 4:
    anti_z444 = 1


try:  # noqa: WPS225
    do_some_bad()
except ValueError:
    print('value')
except KeyError:
    print('key')
except IndexError as exc:
    print('index', exc)
except TypeError:
    print('type')


class BadClass:  # noqa: WPS306
    UPPER_CASE_ATTRIBUTE = 12  # noqa: WPS115

    @staticmethod  # noqa: WPS602
    def some_static(arg1):
        return [
            target  # noqa: WPS224
            for assignment in range(hex_number)
            for target in range(assignment)
            for _ in range(10)
            if isinstance(target, int)
        ]

    @staticmethod  # noqa: WPS602
    async def some_async_static(arg1):
        return [
            node for node in 'ab' if node != 'a' if node != 'b'  # noqa: WPS307
        ]

    def __del__(self, *_args, **_kwargs):  # noqa: WPS603
        anti_z444 = 1  # noqa: WPS442

    class Nested:  # noqa: WPS306,WPS431
        anti_z444 = 1

    async def __eq__(self, other):  # noqa: WPS610
        anti_z444 = 3  # noqa: WPS442


magic_numbers = 13.2 + 50  # noqa: WPS432

assert 1 < 1 < hex_number  # noqa: WPS308
assert 2 > octal_number  # noqa: WPS309

hex_number = 0XFF  # noqa: WPS310
octal_number = 0O11  # noqa: WPS310
binary_number = 0B1001  # noqa: WPS310
number_with_scientific_notation = 1.5E-10  # noqa: WPS310
number_with_useless_plus = +5  # noqa: WPS330

if '6' in nodes in '6':  # noqa: WPS311, WPS525
    anti_z444 = 1

assert hex_number == hex_number  # noqa: WPS312


async def test_async_function():
    return(123, 33)  # noqa: WPS313


if True:  # noqa: WPS314
    anti_z444 = 1


class SomeTestClass(FirstParent, SecondParent, object):  # noqa: WPS315
    anti_z444 = 1


class SomeClass(FirstParent,  # noqa: WPS317
                SecondParent,  # noqa: WPS318
                ThirdParent):  # noqa: WPS319
    anti_z444 = 1


if SomeClass:
        print(SomeClass)  # noqa: WPS318

print(
    1,
    2)  # noqa: WPS319


def function(  # noqa: WPS320
    arg: Optional[  # noqa: WPS320
        str,
    ]
) -> Optional[
    str,
]:
    some_set = {1
               }  # noqa: WPS318


string_modifier = R'(s)'  # noqa: WPS321
multiline_string = """abc"""  # noqa: WPS322


def function_with_wrong_return():
    if some:
        print(some)
    return  # noqa: WPS324


def function_with_wrong_yield():
    if some:
        yield  # noqa: WPS325
    yield 1

bad_concatenation = 'a' 'b'  # noqa: WPS326

for literal in bad_concatenation:  # noqa: WPS327, WPS328
    continue

with open(bad_concatenation):  # noqa: WPS328
    pass  # noqa: WPS420


try:
    anti_z444 = 1
except Exception as ex:  # noqa: WPS329
    raise ex

def some_other_function():
    some_value = 1
    return some_value  # noqa: WPS331

some_cond = cond() and 1 or None  # noqa: WPS332

print(one > two and two > three)  # noqa: WPS333

print(biggesst > middle >= smallest)  # noqa: WPS334

for index in [1, 2]:  # noqa: WPS335
    print(index)

string_concat = 'a' + 'b'  # noqa: WPS336

print(one == 'a' or one == 'b')  # noqa: WPS514
file_obj = open('filaname.py')  # noqa: WPS515
print(type(file_obj) == int)  # noqa: WPS516

print(*[], **{'@': 1})  # noqa: WPS517, WPS445
pi = 3.14 # noqa: WPS446
print(lambda: 0)  # noqa: WPS522
xterm += xterm + 1  # noqa: WPS524

for range_len in range(len(file_obj)):  # noqa: WPS518
    print(range_len)

sum_container = 0
for sum_item in file_obj:  # noqa: WPS519
    sum_container += sum_item

print(sum_container == [])  # noqa: WPS520
print(sum_container is 0)  # noqa: WPS521

try:
    anti_z444 = 1
except BaseException:  # noqa: WPS424
    anti_z444 = 1

call_with_positional_bool(True)  # noqa: WPS425


class MyInt(int):  # noqa: WPS600
    """My custom int subclass."""


class ShadowsAttribute(object):
    """Redefines attr from class."""

    first: int
    second = 1

    def __init__(self) -> None:
        self.first = 1
        self.second = 2  # noqa: WPS601


for symbol in 'abc':  # noqa: WPS500
    anti_z444 = 1
else:
    anti_z444 = 1

try:  # noqa: WPS501
    anti_z444 = 1
finally:
    anti_z444 = 1

nodes = nodes  # noqa: WPS434


class Example(object):
    """Correct class docstring."""

    def __init__(self):  # noqa: WPS611
        """Correct function docstring."""
        yield 10

    def __eq__(self, object_: object) -> bool:  # noqa: WPS612
        return super().__eq__(object_)


for loop_index in range(6):  # noqa: WPS426
    print(lambda: loop_index)


async def function_with_unreachable():
    await test_function()
    raise ValueError()
    print(1)  # noqa: WPS427


1 + 2  # noqa: WPS428

first = second = 2  # noqa: WPS429

first, nodes[0] = range(2)  # noqa: WPS414


try:  # noqa: WPS415
    anti_z444 = 1
except ValueError:
    anti_z444 = 1
except ValueError:
    anti_z444 = 1

iters = list((yield letter) for letter in 'ab')  # noqa: WPS416


class MyBadException(BaseException):  # noqa: WPS418
    anti_z444 = 1


some_if_expr = True if some_set else False  # noqa: WPS502

if some_if_expr:  # noqa: WPS502
    some_dict['x'] = True
else:
    some_dict['x'] = False


class ClassWithWrongContents((lambda: object)()):  # noqa: WPS606
    __slots__ = ['a', 'a']  # noqa: WPS607

    for _ in range(1):  # noqa: WPS604
        anti_z444 = 1

    def method_with_no_args():  # noqa: WPS605
        super(ClassWithWrongContents, self).method_with_no_args()  # noqa: WPS608
        self.some_set = {1, 1}  # noqa: WPS417


def useless_returning_else():
    if some_set:
        return some_set
    else:
        return TypeError  # noqa: WPS503


def multiple_return_path():
    try:  # noqa: WPS419
        return 1
    except Exception:
        return 2
    else:
        return 3


def bad_default_values(
    self,
    withDoctest='PYFLAKES_DOCTEST' in os.environ,  # noqa: WPS404
):
    return True


for nodes[0] in (1, 2, 3):  # noqa: WPS405
    anti_z444 = 1

with open('some') as MyBadException.custom:  # noqa: WPS406
    anti_z444 = 1


anti_z444.__truediv__(1)  # noqa: WPS609

if not some: # noqa: WPS504
    print('False')
else:
    print('Wrong')

try:
    try:  # noqa: WPS505
        anti_z444 = 1
    except ValueError:
        raise TypeError('Second')
except TypeError:
    print('WTF?')

if some and (  # noqa: WPS337
    anti_z444 == 1
):
    anti_z444 = 'some text'


class WrongMethodOrder(object):  # noqa: WPS338
    def _protected(self):
        return self

    def public(self):
        return self


leading_zero = 1.2e01  # noqa: WPS339
positive_exponent = 1.1e+1  # noqa: WPS340
wrong_hex = 0xabc  # noqa: WPS341
wrong_escape_raw_string = '\\n'  # noqa: WPS342
bad_complex = 1J  # noqa: WPS343
zero_div = bad_complex / 0.0  # noqa: WPS344
mult_one = zero_div * 1  # noqa: WPS345
mult_one -= -1  # noqa: WPS346

CONSTANT = []  # noqa: WPS407

numbers = map(lambda string: int(string), ['1'])  # noqa: WPS506

if len(numbers) > 0:  # noqa: WPS507
    print('len!')

if numbers and numbers:  # noqa: WPS408
    print('duplicate boolop')

if not numbers == [1]:  # noqa: WPS508
    print('bad compare with not')

if numbers == CONSTANT != [2]:  # noqa: WPS409
    print(1 + (1 if number else 2))  # noqa: WPS509

print(numbers in [])  # noqa: WPS510
print(isinstance(number, int) or isinstance(number, (float, str)))  # noqa: 474
print(isinstance(numbers, (int,)))  # noqa: WPS512

if numbers:
    print('first')
else:
    if numbers:  # noqa: WPS513
        print('other')

def sync_gen():
    yield
    raise StopIteration  # noqa: WPS438

async def async_gen():
    yield
    raise StopIteration  # noqa: WPS438


class CheckStopIteration(object):
    def sync_gen(self):
        yield
        raise StopIteration()  # noqa: WPS438

    async def async_gen(self):
        yield
        raise StopIteration()  # noqa: WPS438

bad_unicode = b'\u1'  # noqa: WPS439
CheckStopIteration = 1  # noqa: WPS440
print(literal)  # noqa: WPS441
unhashable = {[]}  # noqa: WPS443
assert []  # noqa: WPS444
unhashable = [] * 2  # noqa: WPS435

from json import loads  # noqa: WPS347

some_model = (
    MyModel.objects.filter(...)
        .exclude(...)  # noqa: WPS348
)

swap_a = swap_b
swap_b = swap_a  # noqa: WPS523

print(constant[0:7])  # noqa: WPS349
var_a = var_a + var_b  # noqa: WPS350

class ChildClass(ParentClass):
    def some_method(self):
        super().some_other_method() # noqa: WPS613

LOWERCASE_ALPH = "abcdefghijklmnopqrstuvwxyz" # noqa: WPS447

int()  # noqa: WPS351

for wrong_loop in call(  # noqa: WPS352
    1, 2, 3,
):
    print('bad loop')

if a in {1}:  # noqa: WPS525
    print('bad!')


def implicit_yield_from():
    for wrong_yield in call():  # noqa: WPS526

try: # noqa: WPS448
    anti_z444 = 1
except Exception:
    anti_z444 = 1
except ValueError:
    anti_z444 = 1
        yield wrong_yield
