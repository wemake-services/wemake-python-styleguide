# -*- coding: utf-8 -*-

import pytest

if_with_is = 'if {0} is {1}: ...'
if_with_is_not = 'if {0} is not {1}: ...'

if_with_eq = 'if {0} == {1}: ...'
if_with_not_eq = 'if {0} != {1}: ...'
if_with_gt = 'if {0} > {1}: ...'
if_with_lt = 'if {0} < {1}: ...'
if_with_gte = 'if {0} >= {1}: ...'
if_with_lte = 'if {0} <= {1}: ...'

if_with_chained_compares1 = 'if 0 < {0} < {1}: ...'
if_with_chained_compares2 = 'if {0} > {1} > 0: ...'
if_with_chained_compares3 = 'if -1 > {0} > {1} > 0: ...'

if_with_in = 'if {0} in {1}: ...'
if_with_not_in = 'if {0} not in {1}: ...'

ternary = 'ternary = 0 if {0} > {1} else 1'
while_construct = 'while {0} > {1}: ...'
assert_construct = 'assert {0} == {1}'
assert_with_message = 'assert {0} == {1}, "message"'


# Actual fixtures:

@pytest.fixture(params=[
    if_with_is,
    if_with_is_not,

    if_with_eq,
    if_with_not_eq,
    if_with_lt,
    if_with_gt,
    if_with_lte,
    if_with_gte,

    ternary,
    while_construct,
    assert_construct,
    assert_with_message,
])
def simple_conditions(request):
    """Fixture that returns simple conditionals."""
    return request.param


@pytest.fixture(params=[
    if_with_in,
    if_with_not_in,
])
def in_conditions(request):
    """Fixture that returns simple conditionals."""
    return request.param


@pytest.fixture()
def not_in_wrapper():
    """Fixture to replace all `in` operators to `not in` operators."""
    def factory(template: str) -> str:
        return template.replace(
            ' in ',
            ' not in ',
        )
    return factory


@pytest.fixture(params=['not_in_wrapper', 'regular_wrapper'])
def in_not_in(request):
    """Fixture that returns either `not in` or `in` operators."""
    return request.getfixturevalue(request.param)
