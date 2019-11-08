# -*- coding: utf-8 -*-

import pytest

# Assigns:

simple_assign = '{0} = 1'
multiple_assign = '{0} = unmatched_assign = 1'
annotated_assign1 = '{0}: type = 1'
simple_annotation = '{0}: type'
unpacking_assign1 = '{0}, unmatched_assign = (1, 2)'
unpacking_assign2 = 'unmatched_assign, *{0} = (1, 2)'

_assigned_statements = [
    simple_assign,
    multiple_assign,
    annotated_assign1,
    unpacking_assign1,
    unpacking_assign2,
]

_assigned_and_annotation_statements = _assigned_statements + [simple_annotation]


@pytest.fixture(params=_assigned_statements)
def assign_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param


@pytest.fixture(params=_assigned_and_annotation_statements)
def assign_and_annotation_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
