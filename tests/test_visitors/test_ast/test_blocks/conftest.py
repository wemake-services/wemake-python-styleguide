# -*- coding: utf-8 -*-

import pytest

# Assigns:

simple_assign = '{0} = 1'
multiple_assign = '{0} = unmatched_assign = 1'
annotated_assign1 = '{0}: type = 1'
annotated_assign2 = '{0}: type'
unpacking_assign1 = '{0}, unmatched_assign = (1, 2)'
unpacking_assign2 = 'unmatched_assign1, {0}, unmatched_assign2 = (1, 2)'
unpacking_assign3 = '{0}, *unmatched_assign2 = (1, 2)'
unpacking_assign4 = 'unmatched_assign, *{0} = (1, 2)'


@pytest.fixture(params=[
    simple_assign,
    multiple_assign,
    annotated_assign1,
    annotated_assign2,
    unpacking_assign1,
    unpacking_assign2,
    unpacking_assign3,
    unpacking_assign4,
])
def assign_statement(request):
    """Parametrized fixture that contains all possible assign templates."""
    return request.param
