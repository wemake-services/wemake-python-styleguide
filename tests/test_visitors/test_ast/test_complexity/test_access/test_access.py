# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.complexity.access import (
    AccessVisitor,
    TooDeepAccessViolation,
)

subscript_access = 'my_matrix[0][0][0][0]'
attribute_access = 'self.attr.inner.wrapper.value'
mixed_access = 'self.attr[0].wrapper[0]'
mixed_with_calls_access = 'self.attr[0]().wrapper[0][0].bar().foo[0]()'


@pytest.mark.parametrize('code', [
    subscript_access,
    attribute_access,
    mixed_access,
    mixed_with_calls_access,
])
def test_access_normal(
    assert_errors,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Testing that expressions with correct access length work well."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_access_level=4)
    visitor = AccessVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    subscript_access,
    attribute_access,
    mixed_access,
    mixed_with_calls_access,
])
def test_access_incorrect(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    options,
    mode,
):
    """Testing that violations are raised when reaching too long access."""
    tree = parse_ast_tree(mode(code))

    option_values = options(max_access_level=2)
    visitor = AccessVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooDeepAccessViolation])
    assert_error_text(visitor, '4')
