# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooLongTryBodyViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TryExceptVisitor,
)

try_without_except = """
try:
    {0}
finally:
    ...
"""

simple_try_except = """
try:
    {0}
except ValueError:
    ...
"""

try_except_with_else = """
try:
    {0}
except ValueError:
    ...
else:
    ...
"""

full_except_with_else = """
try:
    {0}
except ValueError:
    ...
else:
    ...
finally:
    ...
"""

# Wrong:

wrong_try_without_except = """
try:
    ...
finally:
    {0}
"""

wrong_simple_try_except = """
try:
    ...
except ValueError:
    {0}
"""

wrong_try_except_with_else = """
try:
    ...
except ValueError:
    ...
else:
    {0}
"""


@pytest.mark.parametrize('statements', [
    'print(1)\n    print(2)',
    'm.print(1)\n    m.print(2)\n    m.print(3)',
    'm = 1\n    p = 2\n    c = 3',
])
@pytest.mark.parametrize('code', [
    try_without_except,
    simple_try_except,
    try_except_with_else,
    full_except_with_else,
])
def test_try_body_count_default(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongTryBodyViolation])


@pytest.mark.parametrize('statements', [
    'print(1)\n    print(2)',
    'm.print(1)\n    m.print(2)',
    'm = 1\n    p = 2',
])
@pytest.mark.parametrize('code', [
    try_without_except,
    simple_try_except,
    try_except_with_else,
    full_except_with_else,
])
def test_try_body_count_custom_options(
    assert_errors,
    parse_ast_tree,
    options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    option_values = options(max_try_body_length=2)
    visitor = TryExceptVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('statements', [
    'print(1)',
    'm.print(1)',
    'm = 1',
])
@pytest.mark.parametrize('code', [
    try_without_except,
    simple_try_except,
    try_except_with_else,
    full_except_with_else,
])
def test_try_body_correct_default(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('statements', [
    'print(1)',
    'm.print(1)',
    'm = 1',
    'print(1)',
    'm.print(1)',
    'm = 1',
])
@pytest.mark.parametrize('code', [
    wrong_simple_try_except,
    wrong_try_except_with_else,
    wrong_try_without_except,
])
def test_try_body_different_nodes(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    statements,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code.format(statements))

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
