# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongFunctionCallViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    BAD_FUNCTIONS,
    WrongFunctionCallVisitor,
)

regular_call = '{0}(*args, **kwargs)'
assignment_call = 'test_result = {0}(*args, **kwargs)'

nested_function_call = """
def proxy(*args, **kwargs):
    return {0}(*args, **kwargs)
"""


@pytest.mark.parametrize('bad_function', BAD_FUNCTIONS)
@pytest.mark.parametrize('code', [
    regular_call,
    assignment_call,
    nested_function_call,
])
def test_wrong_function_called(
    assert_errors, parse_ast_tree, bad_function, code, default_options,
):
    """Testing that some built-in functions are restricted."""
    tree = parse_ast_tree(code.format(bad_function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongFunctionCallViolation])


def test_wrong_decorator_used(assert_errors, parse_ast_tree, default_options):
    """Testing that some built-in functions are restricted as decorators."""
    tree = parse_ast_tree(
        'some_static = staticmethod(some_function)',
    )

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongFunctionCallViolation])


@pytest.mark.parametrize('good_function', ['len', 'abs', 'max', 'custom'])
@pytest.mark.parametrize('code', [
    regular_call,
    assignment_call,
    nested_function_call,
])
def test_regular_function_called(
    assert_errors, parse_ast_tree, good_function, code, default_options,
):
    """Testing that other functions are not restricted."""
    tree = parse_ast_tree(code.format(good_function))

    visitor = WrongFunctionCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
