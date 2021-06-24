import pytest

from wemake_python_styleguide.violations.consistency import (
    UnsafeGeneratorExpressionViolation,
)
from wemake_python_styleguide.visitors.ast.statements import (
    UnsafeGeneratorExpressionVisitor,
)

unsafe_function = """
first_value = 1
expression = (first_value * index for index in range(5))
first_value = 2
sum_result = sum(expression) # noqa: WPS363
"""

no_variables = """
a = 1
b = (i for i in range(5))
c = sum(b)
"""

single_use = """
first_value = 1
result = sum((first_value * i for i in range(5)))
"""

single_use_variables_assigned = """
first_value = 1
result = sum((first_value * i for i in range(5)))
first_value = 2
"""


@pytest.mark.parametrize('code', [
    unsafe_function,
])
def test_unsafe_gen_expression(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that generator expression is unsafe."""
    tree = parse_ast_tree(code)
    visitor = UnsafeGeneratorExpressionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnsafeGeneratorExpressionViolation])


@pytest.mark.parametrize('code', [
    single_use,
    single_use_variables_assigned,
    no_variables,
])
def test_safe_gen_expression(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that generator expression is unsafe."""
    tree = parse_ast_tree(code)
    visitor = UnsafeGeneratorExpressionVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
