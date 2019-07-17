# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import NestedTryViolation
from wemake_python_styleguide.visitors.ast.exceptions import (
    NestedTryBlocksVisitor,
)

# Correct:

one_try_example = """
try:
    ...
except SomeError:
    ...
else:
    ...
finally:
    ...
"""

two_tries_example = """
try:
    ...
except OneError:
    ...
except TwoError:
    ...

try:
    ...
except:
    ...
"""

# Wrong:

wrong_try_nested_try = """
try:
    try:
        ...
    except:
        ...
except:
    ...
"""

wrong_try_nested_except = """
try:
    ...
except:
    try:
        ...
    except:
        ...
"""

wrong_try_nested_else = """
try:
    ...
except:
    ...
else:
    try:
        ...
    except:
        ...
"""


wrong_try_nested_finally = """
try:
    ...
except:
    ...
else:
    try:
        ...
    except:
        ...
"""


@pytest.mark.parametrize('code', [
    wrong_try_nested_try,
    wrong_try_nested_except,
    wrong_try_nested_else,
    wrong_try_nested_finally,
])
def test_nested_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when try blocks are nested."""
    tree = parse_ast_tree(code)

    visitor = NestedTryBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NestedTryViolation])


@pytest.mark.parametrize('code', [
    one_try_example,
    two_tries_example,
])
def test_correct_try_blocks(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when try block is not nested."""
    tree = parse_ast_tree(code)

    visitor = NestedTryBlocksVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
