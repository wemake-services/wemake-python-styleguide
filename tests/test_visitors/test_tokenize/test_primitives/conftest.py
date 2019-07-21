# -*- coding: utf-8 -*-

import pytest

function_call = 'print({0})'
assignment = 'some_name = {0}'
assignment_with_expression = 'some_sum = {0} + 123'
default_param = 'def function(some={0}): ...'
default_param_with_type = 'def function(some: int = {0}): ...'
statement_with_expression = 'other_var + {0}'


@pytest.fixture(params=[
    function_call,
    assignment,
    assignment_with_expression,
    default_param,
    default_param_with_type,
    statement_with_expression,
])
def primitives_usages(request):
    """Fixture to return possible cases of promitives use cases."""
    return request.param


@pytest.fixture()
def regular_number_wrapper():
    """Fixture to return regular numbers without modifications."""
    def factory(template: str) -> str:
        return template
    return factory


@pytest.fixture()
def negative_number_wrapper():
    """Fixture to return negative numbers."""
    def factory(template: str) -> str:
        return '-{0}'.format(template)
    return factory


@pytest.fixture()
def positive_number_wrapper():
    """Fixture to return positive numbers with explicit ``+``."""
    def factory(template: str) -> str:
        return '+{0}'.format(template)
    return factory


@pytest.fixture(params=[
    'regular_number_wrapper',
    'negative_number_wrapper',
    'positive_number_wrapper',
])
def number_sign(request):
    """Fixture that returns regular, negative, and positive numbers."""
    return request.getfixturevalue(request.param)
