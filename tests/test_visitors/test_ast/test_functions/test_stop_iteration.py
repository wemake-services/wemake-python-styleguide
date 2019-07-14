# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    StopIterationInsideGeneratorViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

stop_iteration_generator_method = """
class CheckStopIteration():
    def check_stop_iteration(self):
        yield
        raise {0}
"""

stop_iteration_generator_function = """
def check_stop_iteration():
    yield
    raise {0}
"""


stop_iteration_bare_method = """
class CheckStopIteration():
    def check_stop_iteration(self):
        raise {0}
"""

stop_iteration_bare_function = """
def check_stop_iteration():
    raise {0}
"""


@pytest.mark.parametrize('code', [
    stop_iteration_generator_method,
    stop_iteration_generator_function,
])
@pytest.mark.parametrize('exception', [
    'StopIteration',
    'StopIteration()',
])
def test_stop_iteration_inside_generators(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that `raise StopIteration` is restricted inside generators."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StopIterationInsideGeneratorViolation])


@pytest.mark.parametrize('code', [
    stop_iteration_bare_method,
    stop_iteration_bare_function,
])
@pytest.mark.parametrize('exception', [
    'StopIteration',
    'StopIteration()',
])
def test_stop_iteration_inside_bare_functions(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that `raise StopIteration` is allowed inside bare functions."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    stop_iteration_generator_method,
    stop_iteration_generator_function,
])
@pytest.mark.parametrize('exception', [
    'RuntimeError',
    'RuntimeError()',
])
def test_other_exceptions_inside_generators(
    assert_errors,
    parse_ast_tree,
    code,
    exception,
    default_options,
    mode,
):
    """Testing that `raise` of other exceptions is allowed inside generators."""
    tree = parse_ast_tree(mode(code.format(exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    stop_iteration_generator_method,
    stop_iteration_generator_function,
])
def test_bare_raise_inside_generators(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that bare `raise` is allowed inside generators."""
    tree = parse_ast_tree(code)

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
