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

safe_no_variables = """
first_value = 1
result = (index for index in range(5))
c = sum(result)
"""

safe_single_use = """
first_value = 1
result = sum((first_value * i for i in range(5)))
"""

safe_single_use_variables = """
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

unsafe_self_aug_value = """
values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in values)
self.exponent += 1
print(list(power_expr))
"""

safe_self_aug_value = """
values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in values)
print(list(power_expr))
self.exponent += 1
"""

unsafe_self = """
values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in values)
self.exponent = 1
print(list(power_expr))
"""

safe_self = """
values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in values)
print(list(power_expr))
self.exponent = 1
"""

unsafe_append = """
values = [1, 2, 3, 4, 5]
power_expr = (value for value in values)
values.append(6)
print(list(power_expr))
"""

safe_append = """
values = [1, 2, 3, 4, 5]
power_expr = (value for value in values)
print(list(power_expr))
values.append(6)
"""

unsafe_self_values = """
self.values = [1, 2, 3, 4, 5]
power_expr = (value for value in self.values)
self.values.append(6)
print(list(power_expr))
"""

safe_self_values = """
self.values = [1, 2, 3, 4, 5]
power_expr = (value for value in self.values)
print(list(power_expr))
self.values.append(6)
"""

safe_double_self = """
self.values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in self.values)
print(list(power_expr))
self.exponent = 1
"""

unsafe_double_self = """
self.values = [1, 2, 3, 4, 5]
self.exponent = 5
power_expr = (value * self.exponent for value in self.values)
self.exponent = 1
print(list(power_expr))
"""

safe_assign = """
values = [1, 2, 3, 4, 5]
exponent = 5
self.power_expr = (value * exponent for value in values)
print(list(self.power_expr))
exponent = 1
"""

unsafe_assign = """
values = [1, 2, 3, 4, 5]
exponent = 5
self.power_expr = (value * exponent for value in values)
exponent = 1
print(list(self.power_expr))
"""

safe_assign_append = """
values = [1, 2, 3, 4, 5]
exponent = 5
self.power_expr = (value * exponent for value in values)
print(list(self.power_expr))
values.append(6)
"""

unsafe_assign_append = """
values = [1, 2, 3, 4, 5]
exponent = 5
self.power_expr = (value * exponent for value in values)
values.append(6)
print(list(self.power_expr))
"""

safe_gen_no_called = """
values = [1, 2, 3, 4, 5]
power_expr = (value for value in values)
values.append(6)
"""


@pytest.mark.parametrize('code', [
    unsafe_function,
    unsafe_string,
    unsafe_change_index,
    unsafe_aug_value,
    unsafe_append,
    unsafe_self,
    unsafe_self_values,
    unsafe_double_self,
    unsafe_self_aug_value,
    unsafe_assign,
    unsafe_assign_append,
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
    safe_single_use,
    safe_single_use_variables,
    safe_no_variables,
    safe_string,
    safe_change_index,
    safe_aug_value,
    safe_self,
    safe_append,
    safe_self_values,
    safe_self_aug_value,
    safe_double_self,
    safe_assign,
    safe_assign_append,
    safe_gen_no_called,
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
