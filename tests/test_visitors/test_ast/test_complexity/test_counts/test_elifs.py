# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyElifsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import ElifVisitor

module_with_one_elif = """
if 1 > 2:
    ...
elif 2 > 3:
    ...
else:
    ...
"""

module_with_two_elifs = """
if 1 > 2:
    ...
elif 2 > 3:
    ...
elif 3 > 4:
    ...
else:
    ...
"""

module_with_three_elifs = """
if 1 > 2:
    ...
elif 2 > 3:
    ...
elif 3 > 4:
    ...
elif 4 > 5:
    ...
else:
    ...
"""

module_with_elifs = """
if 1 > 2:
    ...
elif 2 > 3:
    ...
elif 3 > 4:
    ...
elif 4 > 5:
    ...
elif 5 > 6:
    ...
else:
    ...
"""

module_with_elifs_without_else = """
if 1 > 2:
    ...
elif 2 > 3:
    ...
elif 3 > 4:
    ...
elif 4 > 5:
    ...
elif 5 > 6:
    ...
"""

function_with_one_elif = """
def test_module():
    if 1 > 2:
        ...
    elif 2 > 3:
        ...
    else:
        ...
"""

function_with_two_elifs = """
def test_module():
    if 1 > 2:
        ...
    elif 2 > 3:
        ...
    elif 3 > 4:
        ...
    else:
        ...
"""

function_with_three_elifs = """
def test_module():
    if 1 > 2:
        ...
    elif 2 > 3:
        ...
    elif 3 > 4:
        ...
    elif 4 > 5:
        ...
    else:
        ...
"""

function_with_elifs = """
def test_module():
    if 1 > 2:
        ...
    elif 2 > 3:
        ...
    elif 3 > 4:
        ...
    elif 4 > 5:
        ...
    elif 5 > 6:
        ...
    else:
        ...
"""

function_with_elifs_without_else = """
def test_module():
    if 1 > 2:
        ...
    elif 2 > 3:
        ...
    elif 3 > 4:
        ...
    elif 4 > 5:
        ...
    elif 5 > 6:
        ...
"""

function_with_ifs = """
def test_module():
    if True:
        ...
    if 2 > 3:
        ...
    if 3 > 4:
        ...
"""

function_with_raw_if = """
def function():
    if 1 == 2:
        ...
"""

function_with_if_else = """
def function(param):
    if param == 2:
        ...
    else:
        ...
"""

function_with_ternary = """
def with_ternary(some_value):
    return [some_value] if some_value > 1 else []
"""


@pytest.mark.parametrize('code', [
    module_with_one_elif,
    module_with_two_elifs,
    module_with_three_elifs,
    function_with_one_elif,
    function_with_two_elifs,
    function_with_three_elifs,
    function_with_ifs,
    function_with_raw_if,
    function_with_if_else,
    function_with_ternary,
])
def test_elif_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that all `if`/`elif`/`else` is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = ElifVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    module_with_elifs,
    module_with_elifs_without_else,
    function_with_elifs,
    function_with_elifs_without_else,
])
def test_elif_incorrect_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that incorrect number of `elif` is restricted."""
    tree = parse_ast_tree(code)

    visitor = ElifVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyElifsViolation])
    assert_error_text(visitor, '4', baseline=3)
