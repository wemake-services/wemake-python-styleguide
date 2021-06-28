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
first_value = 1
result = (index for index in range(5))
c = sum(result)
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

unsafe_string = """
line = ['child','tall']
suffix = 'ish'
converted_words = (word + suffix for word in line)
suffix = 'ash'
print(list(converted_words))
"""

safe_string = """
line = ['hello', 'world']
suffix = 'rar'
converted_words = (word + suffix for word in line)
print(list(converted_words))
"""

unsafe_change_index = """
values = [1, 2, 3, 4, 5]
exponent = 5
power_expr = (value * exponent for value in values)
exponent = 10
print(list(power_expr))
"""

safe_change_index = """
values = [1, 2, 3, 4, 5]
exponent = 5
power_expr = (value * exponent for value in values)
print(list(power_expr))
exponent = 10
"""

unsafe_aug_value = """
values = [1, 2, 3, 4, 5]
exponent = 5
power_expr = (value * exponent for value in values)
exponent += 1
print(list(power_expr))
"""

safe_aug_value = """
values = [1, 2, 3, 4, 5]
exponent = 5
power_expr = (value * exponent for value in values)
print(list(power_expr))
exponent += 1
"""


@pytest.mark.parametrize('code', [
    unsafe_function,
    unsafe_string,
    unsafe_change_index,
    unsafe_aug_value,
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
    safe_string,
    safe_change_index,
    safe_aug_value,
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
