# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.ast.classes import (
    WrongClassVisitor,
)
from wemake_python_styleguide.violations.best_practices import (
    YieldInsideInitViolation,
)

init_without_yield = """
class ModuleMembersVisitor(object):
    def __init__(self, *args, **kwargs):
        self._public_items_count = 0
"""

init_with_yield = """
class ModuleMembersVisitor(object):
    def __init__(self, *args, **kwargs):
        yield 10
"""

async_init_without_yield = """
class ModuleMembersVisitor(object):
    async def __init__(self, *args, **kwargs):
        self._public_items_count = 0
"""

async_init_with_yield = """
class ModuleMembersVisitor(object):
    async def __init__(self, *args, **kwargs):
        yield 10
"""


@pytest.mark.parametrize('code', [
    init_with_yield,
    async_init_with_yield,
])
def test_init(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `__init__` without `yield` is prohibited"""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [YieldInsideInitViolation])


@pytest.mark.parametrize('code', [
    init_without_yield,
    async_init_without_yield,
])
def test_init(
    assert_errors, parse_ast_tree, code, default_options,
):
    """Testing that `__init__` without `yield` is allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
