# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitElifViolation,
)
from wemake_python_styleguide.visitors.tokenize.conditions import IfElseVisitor

# Correct:

elif_cases = """
if some:
    ...
elif other:
    ...
elif third:
    ...
else:
    ...
"""

if_expression_in_else = """
if some:
    ...
else:
    print('a' if some else 'b')
"""

not_direct_parent = """
if some:
    ...
else:
    for char in 'abc':
        if char:
            ...
"""

# Wrong:

implicit_elif = """
if some:
    ...
else:
    if other:
        ...
"""

# False positives, triggered by other constructs with `else` clause
# (see https://github.com/wemake-services/wemake-python-styleguide/issues/835)

for_else = """
for a in b:
   ...
else:
   if some:
       ...
"""

try_except_else = """
try:
   ...
except:
   ...
else:
   if some:
       ...
"""

embedded_else = """
... if ... else ...
"""

technically_correct_token_stream = """
    42
        a
    else
"""


@pytest.mark.parametrize('code', [
    elif_cases,
    if_expression_in_else,
    not_direct_parent,
])
def test_correct_if_statements(
    code,
    assert_errors,
    parse_tokens,
    default_options,
):
    """Testing regular conditions."""
    file_tokens = parse_tokens(code)

    visitor = IfElseVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    implicit_elif,
])
def test_implicit_elif_statements(
    code,
    assert_errors,
    parse_tokens,
    default_options,
):
    """Testing implicit `elif` conditions."""
    file_tokens = parse_tokens(code)

    visitor = IfElseVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [ImplicitElifViolation])


@pytest.mark.parametrize('code', [
    for_else,
    try_except_else,
    embedded_else,
    technically_correct_token_stream,
])
def test_false_positives_are_ignored(
    code,
    assert_errors,
    parse_tokens,
    default_options,
):
    """Testing regular conditions."""
    file_tokens = parse_tokens(code)

    visitor = IfElseVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
