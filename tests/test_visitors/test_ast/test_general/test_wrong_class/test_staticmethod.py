# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    StaticMethodViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassVisitor

decorated_method = """
class Example(object):
    @{0}
    def should_fail(): ...
"""

async_decorated_method = """
class Example(object):
    @{0}
    async def should_fail(): ...
"""


@pytest.mark.parametrize('code', [
    decorated_method,
    async_decorated_method,
])
def test_staticmethod_used(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that some built-in functions are restricted as decorators."""
    tree = parse_ast_tree(code.format('staticmethod'))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StaticMethodViolation])


@pytest.mark.parametrize('code', [
    decorated_method,
    async_decorated_method,
])
@pytest.mark.parametrize('decorator', [
    'classmethod',
    'custom',
    'with_params(12, 100)',
])
def test_regular_decorator_used(
    assert_errors,
    parse_ast_tree,
    decorator,
    code,
    default_options,
):
    """Testing that other decorators are allowed."""
    tree = parse_ast_tree(code.format(decorator))

    visitor = WrongClassVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
