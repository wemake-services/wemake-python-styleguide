import pytest

from wemake_python_styleguide.violations.best_practices import (
    StopIterationInsideGeneratorViolation,
)
from wemake_python_styleguide.visitors.ast.functions import (
    FunctionDefinitionVisitor,
)

stop_iteration_method = """
class CheckStopIteration():
    def check_stop_iteration(self):
        {0}
        raise {1}
"""

stop_iteration_function = """
def check_stop_iteration():
    {0}
    raise {1}
"""


@pytest.mark.parametrize('code', [
    stop_iteration_method,
    stop_iteration_function,
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield some_parameter',
])
@pytest.mark.parametrize('exception', [
    'StopIteration',
    'StopIteration()',
    'StopIteration(1)',
])
def test_stop_iteration_inside_generators(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    exception,
    default_options,
    mode,
):
    """Testing that `raise StopIteration` is restricted inside generators."""
    tree = parse_ast_tree(mode(code.format(statement, exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StopIterationInsideGeneratorViolation])


@pytest.mark.parametrize('code', [
    stop_iteration_method,
    stop_iteration_function,
])
@pytest.mark.parametrize('statement', [
    'yield from generator()',
])
@pytest.mark.parametrize('exception', [
    'StopIteration',
    'StopIteration()',
    'StopIteration(1)',
])
def test_stop_iteration_in_generators_yield_from(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    exception,
    default_options,
):
    """Testing that `raise StopIteration` is restricted inside generators."""
    tree = parse_ast_tree(code.format(statement, exception))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StopIterationInsideGeneratorViolation])


@pytest.mark.parametrize('code', [
    stop_iteration_method,
    stop_iteration_function,
])
@pytest.mark.parametrize('statement', [
    'print("not a generator")',
])
@pytest.mark.parametrize('exception', [
    'StopIteration',
    'StopIteration()',
    'StopIteration(1)',
])
def test_stop_iteration_inside_bare_functions(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    exception,
    default_options,
    mode,
):
    """Testing that `raise StopIteration` is allowed inside bare functions."""
    tree = parse_ast_tree(mode(code.format(statement, exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    stop_iteration_method,
    stop_iteration_function,
])
@pytest.mark.parametrize('statement', [
    'yield',
    'yield some_parameter',
])
@pytest.mark.parametrize('exception', [
    'RuntimeError',
    'RuntimeError()',
    'RuntimeError(1)',
])
def test_other_exceptions_inside_generators(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    exception,
    default_options,
    mode,
):
    """Testing that `raise` of other exceptions is allowed inside generators."""
    tree = parse_ast_tree(mode(code.format(statement, exception)))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    stop_iteration_method,
    stop_iteration_function,
])
@pytest.mark.parametrize('statement', [
    'yield from generator()',
])
@pytest.mark.parametrize('exception', [
    'RuntimeError',
    'RuntimeError()',
    'RuntimeError(1)',
])
def test_other_exc_in_generators_yield_from(
    assert_errors,
    parse_ast_tree,
    code,
    statement,
    exception,
    default_options,
):
    """Testing that `raise` of other exceptions is allowed inside generators."""
    tree = parse_ast_tree(code.format(statement, exception))

    visitor = FunctionDefinitionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
