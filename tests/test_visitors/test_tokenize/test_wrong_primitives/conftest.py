# -*- coding: utf-8 -*-

import pytest

function_call = 'print({0})'
assignment = 'some_name = {0}'
assignment_with_expression = 'some_sum = {0} + 123'
default_param = 'def function(some={0}): ...'
default_param_with_type = 'def function(some: int = {0}): ...'
statement = '{0}'
statement_with_expression = '{0} + other_var'


@pytest.fixture(params=[
    function_call,
    assignment,
    assignment_with_expression,
    default_param,
    default_param_with_type,
    statement,
    statement_with_expression,
])
def primitives_usages(request):
    """Fixture to return possible cases of promitives use cases."""
    return request.param
