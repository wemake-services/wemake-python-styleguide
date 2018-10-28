# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    YieldInsideInitViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

init_without_yield = """
class ModuleMembersVisitor(object):
    def __init__(self, *args, **kwargs):
        self._public_items_count = 0
"""

init_with_yield = """
class ModuleMembersVisitor(object):
    def __init__(self, *args, **kwargs):
        yield self
"""

regular_method_with_yield = """
class ModuleMembersVisitor(object):
    def method(self, *args, **kwargs):
        yield self
"""

iter_with_yield = """
class ModuleMembersVisitor(object):
    def __iter__(self, *args, **kwargs):
        yield self
"""


def test_init_generator(
    assert_errors,
    parse_ast_tree,
    default_options,
    mode,
):
    """Testing that `__init__` without `yield` is prohibited."""
    tree = parse_ast_tree(mode(init_with_yield))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [YieldInsideInitViolation])


@pytest.mark.parametrize('code', [
    init_without_yield,
    regular_method_with_yield,
    iter_with_yield,
])
def test_init_regular(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing that `__init__` without `yield` is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
