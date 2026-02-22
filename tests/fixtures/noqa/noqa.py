"""
This file contains all possible violations.

It is used for e2e tests.
"""

from __future__ import print_function  # noqa: WPS422

from typing import List

import os.path  # noqa: WPS301

from foo import bar
from foo.bar import baz  # noqa: WPS458
from package import module, module as alias  # noqa: WPS474

from .version import get_version  # noqa: WPS300

import import1
import import2
import import3
import import4

from some_name import (  # noqa: WPS235
    name1,
    name2,
    name3,
    name4,
    name5,
    name6,
    name7,
    name8,
    name9,
    name10,
    name11,
    name12,
    name13,
    name14,
    name15,
    name16,
    name17,
    name18,
    name19,
    name20,
    name21,
    name22,
    name23,
    name24,
    name25,
    name26,
    name27,
    name28,
    name29,
    name30,
    name31,
    name32,
    name33,
    name34,
    name35,
    name36,
    name37,
    name38,
)

# Raising and ignoring:
some_int = 1  # type: int


# =====

phone_number = 8_83_134_43  # noqa:  WPS303
float_zero = 0.0  # noqa: WPS358
formatted_string_complex = f'1+1={1 + 1}'  # noqa: WPS237


def __getattr__():  # noqa: WPS413
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/461
    ...


def foo_func():
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/601

    yield (1, 2, 3, 4, 5, 6)  # noqa: WPS227


my_print(x > 2 > y > 4)  # noqa: WPS228

try:  # noqa: WPS229
    my_print(1)
    my_print(2)
    my_print(3)
except AnyError:
    my_print('nope')


class TooManyPublicAtts:  # noqa: WPS230
    def __init__(self):
        self.first = 1
        self.second = 2
        self.third = 3
        self.fourth = 4
        self.fifth = 5
        self.sixth = 6
        self.boom = 7


@property
def function_name(  # noqa: WPS614
    value: int = 0,  # noqa: WPS110
):
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/392
    ...


def some():  # noqa: WPS110
    class Nested:  # noqa: WPS431
        """Docs."""

    def nested():  # noqa: WPS430
        ...

    if some_condition():
        def deep_nested():  # noqa: WPS430
            ...
    else:
        async def deep_nested():  # noqa: WPS430
            ...


del {'a': 1}['a']  # noqa: WPS420
delattr(object, 'some')  # noqa: WPS421
value = 1  # noqa: WPS110
VALUE = 1  # noqa: WPS110
x = 2  # noqa: WPS111
__private = 3  # noqa: WPS112
star_wars_episode_7 = 'the worst episode ever after 8 and 9'  # noqa: WPS114
consecutive__underscores = 4  # noqa: WPS116
cls = 5  # noqa: WPS117
__author__ = 'Nikita Sobolev'  # noqa: WPS410
extremely_long_name_that_needs_to_be_shortened_to_work_fine = 2  # noqa: WPS118
wrong_alias_ = 'some fake builtin alias'  # noqa: WPS120

def some_function():
    _should_not_be_used = 1  # noqa: WPS122
    my_print(_should_not_be_used)  # noqa: WPS121

used, __ = 1, 2  # noqa: WPS123

class Mem0Output:  # noqa: WPS124
    # See:
    # https://github.com/wemake-services/wemake-python-styleguide/issues/1191
    anti_wps124 = 'unreadable class'


def many_locals():  # noqa: WPS210
    arg1, arg2, arg3, arg4, arg5, arg6 = range(6)  # noqa: WPS236


def many_arguments(_arg1, _arg2, _arg3, _arg4, _arg5, _arg6):  # noqa: WPS211
    ...


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
    my_print(xy)
    my_print(xy)
    my_print(xy)

    my_print(xy)
    my_print(xy)
    my_print(xy)

    my_print(xy)
    my_print(xy)
    my_print(xy)

    my_print(xy)


class TooManyMethods:  # noqa: WPS214
    def method1(self):
        ...

    def method2(self):
        ...

    def method3(self):
        ...

    def method4(self):
        ...

    def method5(self):
        ...

    def method6(self):
        ...

    def method7(self):
        ...

    def method8(self):
        ...


class ManyParents(First, Second, Third, Exception):  # noqa: WPS215
    """Docs."""


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
    ...

if line:  # noqa: WPS223
    ...
elif line > 1:
    ...
elif line > 2:
    ...
elif line > 3:
    ...
elif line > 4:
    ...


try:  # noqa: WPS225
    do_some_bad()
except ValueError:
    my_print('value')
except KeyError:
    my_print('key')
except IndexError as exc:
    my_print('index', exc)
except TypeError:
    my_print('type')


class BadClass:
    UPPER_CASE_ATTRIBUTE = 12  # noqa: WPS115

    def __del__(self, *_args, **_kwargs):  # noqa: WPS603
         my_print('del')

    class Nested:  # noqa: WPS431
        """Docs."""

    async def __eq__(self, other):  # noqa: WPS610
        my_print('eq')


magic_numbers = 13.2 + 50  # noqa: WPS432

assert 1 < 1 < hex_number  # noqa: WPS308

number_with_useless_plus = +5  # noqa: WPS330

if '6' in nodes in '6':  # noqa: WPS311
    ...


if True:  # noqa: WPS314
    ...



string_modifier = R'(\n)'  # noqa: WPS321
multiline_string = """abc"""  # noqa: WPS322


def function_with_wrong_return():
    if some:
        my_print(some)
    return  # noqa: WPS324


def function_with_wrong_yield():
    if some:
        yield  # noqa: WPS325
    yield 1

for literal in bad_concatenation:  # noqa: WPS327, WPS328, WPS481
    continue

with open(bad_concatenation):  # noqa: WPS328
    pass  # noqa: WPS420


my_print(biggesst > middle >= smallest)  # noqa: WPS334

for index in [1, 2]:  # noqa: WPS335, WPS481
    my_print(index)

string_concat = 'a' + 'b'  # noqa: WPS336

file_obj = open('filaname.py')  # noqa: WPS515
my_print(type(file_obj) == int)  # noqa: WPS516

my_print(*[], **{'@': 1})  # noqa: WPS517, WPS445
pi = 3.14 # noqa: WPS446
my_print(lambda: 0)  # noqa: WPS522
xterm += xterm + 1  # noqa: WPS524

for range_len in range(len(file_obj)):  # noqa: WPS518, WPS481
    my_print(range_len)

sum_container = 0
for sum_item in file_obj:  # noqa: WPS519, WPS481
    sum_container += sum_item

my_print(sum_container == [])  # noqa: WPS520


class MyInt(int):  # noqa: WPS600
    """My custom int subclass."""


class ShadowsAttribute:
    """Redefines attr from class."""

    first: int
    second = 1

    def __init__(self) -> None:
        self.first = 1
        self.second = 2  # noqa: WPS601


for symbol in 'abc':  # noqa: WPS500, WPS481
    ...
else:
    ...

try:  # noqa: WPS501
    ...
finally:
    ...


class Example:
    """Correct class docstring."""

    def __init__(self):  # noqa: WPS611
        """Correct function docstring."""
        yield 10

    def __eq__(self, object_: object) -> bool:  # noqa: WPS612
        return super().__eq__(object_)


for loop_index in range(6):  # noqa: WPS426, WPS481
    my_print(lambda: loop_index)


async def function_with_unreachable():
    await test_function()
    raise ValueError()
    my_print(1)  # noqa: WPS427


first = second = 2  # noqa: WPS429

first, nodes[0] = range(2)  # noqa: WPS414


class MyBadException(BaseException):  # noqa: WPS418
    """Docs."""



class ClassWithWrongContents((lambda: object)()):  # noqa: WPS606
    __slots__ = ['a', 'a']  # noqa: WPS607

    for bad_body_node in range(1):  # noqa: WPS481, WPS604
        anti_wps604 = 1

    def method_with_no_args():  # noqa: WPS605
        based = super(ClassWithWrongContents, self).method_with_no_args()  # noqa: WPS608
        my_print(based)


def bad_default_values(
    self,
    withDoctest='PYFLAKES_DOCTEST' in os.environ,  # noqa: WPS404
):
    return True


for nodes[0] in (1, 2, 3):  # noqa: WPS405, WPS481
    ...

with open('some') as MyBadException.custom:  # noqa: WPS406
    ...

if not some: # noqa: WPS504
    my_print('False')
else:
    my_print('Wrong')

try:
    try:  # noqa: WPS505
        ...
    except ValueError:
        raise TypeError('Second')
except TypeError:
    my_print('WTF?')


class WrongMethodOrder:  # noqa: WPS338
    def _protected(self):
        return self

    def public(self):
        return self


leading_zero = 1.2e01  # noqa: WPS339
wrong_escape_raw_string = '\\n'  # noqa: WPS342
zero_div = bad_complex / 0  # noqa: WPS344
mult_one = zero_div * 1  # noqa: WPS345
mult_one -= -1  # noqa: WPS346

CONSTANT = []  # noqa: WPS407

numbers = map(lambda string: int(string), ['1'])  # noqa: WPS506

if numbers and numbers:  # noqa: WPS408, WPS366
    my_print('duplicate boolop')

if numbers == CONSTANT != [2]:  # noqa: WPS409
    my_print(1 + (1 if number else 2))  # noqa: WPS509

if numbers:
    my_print('first')
else:
    if numbers == [1, 2]:  # noqa: WPS513
        my_print('other')

def sync_gen():
    yield
    raise StopIteration  # noqa: WPS438

async def async_gen():
    yield
    raise StopIteration  # noqa: WPS438


class CheckStopIteration:
    def sync_gen(self):
        yield
        raise StopIteration()  # noqa: WPS438

    async def async_gen(self):
        yield
        raise StopIteration()  # noqa: WPS438

bad_unicode = b'\u0040'  # noqa: WPS439
my_print(literal)  # noqa: WPS441
unhashable = {[]}  # noqa: WPS443
assert []  # noqa: WPS444
unhashable = [] * 2  # noqa: WPS435

from json import loads  # noqa: WPS347

swap_a = swap_b
swap_b = swap_a  # noqa: WPS523

my_print(constant[0:7])  # noqa: WPS349
var_a = var_a + var_b  # noqa: WPS350

class ChildClass(ParentClass):
    def some_method(self):
        super().some_other_method() # noqa: WPS613

LOWERCASE_ALPH = "abcdefghijklmnopqrstuvwxyz" # noqa: WPS447

try: # noqa: WPS448
    ...
except Exception:
    ...
except ValueError:
    ...


bad_frozenset = frozenset([1]) # noqa: WPS527


def wrong_yield_from():
    yield from []  # noqa: WPS353


if 'key' in some_dict:
    my_print(some_dict['key'])  # noqa: WPS529
    my_print(other_dict[1.0])  # noqa: WPS449
    my_print(some_sized[len(some_sized) - 2])  # noqa: WPS530

deep_func(a)(b)(c)(d)  # noqa: WPS233

annotated: List[List[List[List[int]]]]  # noqa: WPS234

*numbers, = [4, 7]  # noqa: WPS356, WPS460
[first_number, second_number] = [4, 7]  # noqa: WPS359


class AttributeGetter:
    def __init__(self):
        self.attribute = 1

    def get_attribute(self):  # noqa: WPS615
        return self  # this is not important

    def set_attribute(self):  # noqa: WPS615
        anti_wps = ...


a_list = [1, 2, 3, 4, 5]
a_list[1:3] = [1, 2]  # noqa: WPS362
a_list[slice(1)] = [1, 2]  # noqa: WPS362


def function_with_SystemExit():
    raise SystemExit(1)  # noqa: WPS363


try:
    cause_errors()
except ValueError or TypeError:  # noqa: WPS455
    my_print("Oops.")

def infinite_loop():
    while True:  # noqa: WPS457
        my_print('forever')


my_print(some_float == 1.0)  # noqa: WPS459


def many_raises_function(parameter):  # noqa: WPS238
    if parameter == 1:
        raise ValueError('1')
    if parameter == 2:
        raise KeyError('2')
    if parameter == 3:
        raise IndexError('3')
    raise TypeError('4')


try:
    my_print('try')
except (TypeError, ValueError, LookupError, KeyboardInterrupt):  # noqa: WPS239
    my_print('except')


match inst1, inst2, inst3, inst4, inst5, inst6, inst7, inst8:  # noqa: WPS241
    case 1:
        my_print('except')


match x:  # noqa: WPS242
    case 1:
        my_print('first')
    case 2:
        my_print('second')
    case 3:
        my_print('third')
    case 4:
        my_print('fourth')
    case 5:
        my_print('fifth')
    case 6:
        my_print('sixth')
    case 7:
        my_print('seventh')
    case 8:
        my_print('eighth')

match subject:  # noqa: WPS365
    case 1:
        ...
    case _:
        ...


my_print("""
text
""")  # noqa: WPS462


def get_item():  # noqa: WPS463
    return  # noqa: WPS324

for _, something in enumerate(collection): # noqa: WPS468, WPS481
    report(something)

variable_to_store_things = {
    definitely_something
    for _, definitely_something in enumerate(collection) # noqa: WPS468
}

try:  # noqa: WPS328
    raise TypeError('Type Error')
except TypeError as raise_from_itself:
    my_print(raise_from_itself)
    raise raise_from_itself from raise_from_itself  # noqa: WPS469


class TestClass(**{}):  # noqa: WPS470
    """Docs."""


secondary_slice = items[1:][:3]  # noqa: WPS471
first, *_rest = some_collection  # noqa: WPS472

def foo2_func():
    return (1, 2, 3, 4, 5, 6)  # noqa: WPS227

noqa_wps532 = variable is some_thing is other_thing  # noqa: WPS532

if noqa_wps533:  # noqa: WPS533
    my_print('1')
elif noqa_wps533:
    my_print('2')

noqa_wps534 = second if first == second else first  # noqa: WPS534

match some_value:  # noqa: WPS535
    case SomeClass():
        my_print('first')
    case SomeClass():
        my_print('second')

match [some_value]:  # noqa: WPS536
    case SomeClass():
        my_print('first')

class Baseline:
    def method(self, number):
        return number + 1

class Antediluvian(Baseline):
    def method(self):
        return (super().method(some_item) for some_item in items)  # noqa: WPS616


class LambdaAssign:
    def __init__(self):
        self.attribute = lambda self_arg: int(self_arg) + 1  # noqa: WPS617


# porting noqa38.py
class WithStatic:
    @staticmethod
    def some_static(arg1):  # noqa: WPS602
        my_print('WTF?')

    @staticmethod
    async def some_async_static(arg1):  # noqa: WPS602
        my_print('WTF?')


@first
@second
@third(param='a')
@fourth
@fifth()
@error
def decorated():  # noqa: WPS216
    my_print('WTF?')


def wrong_comprehension1():
    return [  # noqa: WPS307
        node
        for node in 'ab'
        if node != 'a'
        if node != 'b'
    ]


def wrong_comprehension2():
    return [  # noqa: WPS224
        target
        for assignment in range(hex_number)
        for target in range(assignment)
        for _ in range(10)
        if isinstance(target, int)
    ]


for unique_element in range(10):  # noqa: WPS481
    if (other := unique_element) > 5:  # noqa: WPS332
        my_print(1)

    my_print(4)


@some_decorator + other_decorator  # noqa: WPS466
def my_function():
    return 1


user_id = 'uuid-user-id'
match user:
    case 'user_id' | 'uid' as _uid:  # noqa: WPS122
        raise ValueError(_uid)
    case {'key': k}:  # noqa: WPS111
        raise ValueError(k)
    case [objs]:  # noqa: WPS110
        raise ValueError(objs)


def pos_only_problem(first_argpm=0, second_argpm=1, /):  # noqa: WPS475
    my_print(first_argpm, second_argpm)


async def test_await_in_loop():
    for _ in range(10):
        await test_function()  # noqa: WPS476


some_sequence = some_sequence[::-1]  # noqa: WPS478

try: # noqa: WPS243
    my_print("1")
except AnyError:
    my_print("oh no error")
finally:
    my_print("3 / 0")
    my_print('zero division error')
    my_print(3 / 3)
    my_print('no zero division error')

if not user in users:  # noqa: WPS364
    my_print('legacy not-in style')
