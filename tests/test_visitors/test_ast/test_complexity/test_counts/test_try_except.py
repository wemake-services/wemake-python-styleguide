# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyExceptCasesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TryExceptVisitor,
)

try_without_except = """
try:
    ...
finally:
    ...
"""

simple_try_except = """
try:
    ...
except ValueError:
    ...
"""

try_except_with_else = """
try:
    ...
except ValueError:
    ...
else:
    ...
"""

complex_try_except = """
try:
    ...
except ValueError:
    ...
except KeyError:
    ...
except IndexError as exc:
    ...
except TypeError:
    ...
"""


def test_try_except_count_default(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(complex_try_except)

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyExceptCasesViolation])


@pytest.mark.parametrize('code', [
    try_without_except,
    simple_try_except,
    try_except_with_else,
])
def test_try_except_count_custom_settings(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that correct patterns work."""
    tree = parse_ast_tree(code)

    visitor = TryExceptVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
