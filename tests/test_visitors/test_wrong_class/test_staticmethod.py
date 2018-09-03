# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.wrong_class import (
    StaticMethodViolation,
    WrongClassVisitor,
)

decorated_method = """
class Example(object):
    @{0}
    def should_fail(): ...
"""


def test_staticmethod_used(assert_errors, parse_ast_tree, default_options):
    """Testing that some built-in functions are restricted as decorators."""
    tree = parse_ast_tree(decorated_method.format('staticmethod'))

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [StaticMethodViolation])


@pytest.mark.parametrize('decorator', [
    'classmethod',
    'custom',
    'with_params(12, 100)',
])
def test_regular_decorator_used(
    assert_errors, parse_ast_tree, decorator, default_options,
):
    """Testing that other decorators are allowed."""
    tree = parse_ast_tree(decorated_method.format(decorator))

    visiter = WrongClassVisitor(default_options)
    visiter.visit(tree)

    assert_errors(visiter, [])
