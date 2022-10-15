import pytest

from wemake_python_styleguide.violations.oop import BuggySuperContextViolation
from wemake_python_styleguide.visitors.ast.classes import BuggySuperCallVisitor

error_dict_comprehension = """
    {super().make_key(it): make_value(it) for it in items}
"""

error_set_comprehension = """
    {super().transmute(it) for it in items}
"""

error_list_comprehension = """
    [super().transmute(it) for it in items]
"""

error_generator_expression = """
    (super().transmute(it) for it in items)
"""

error_nested_comprehensions = """
    [
        it + 1
        for it in (super().transmute(i) for i in range(10))
    ]
"""

error_nested_methods = """
class B(A):
   def method(self):
       def inner():
           super().method()
"""

error_multiple_nested_comprehensions = """
    [
        it + k + el + 1
        for it in (super().transmute(i) for i in range(10))
        for k in {v:0 for v in range(10)}
        for el in (n ** 2 for n in range(10))
    ]
"""

correct_dict_comprehension = """
    {super(cls, self).make_key(it): make_value(it) for it in items}
"""

correct_set_comprehension = """
    {super(cls, self).transmute(it) for it in items}
"""

correct_list_comprehension = """
    [super(cls, self).transmute(it) for it in items]
"""

correct_generator_expression = """
    (super(cls, self).transmute(it) for it in items)
"""

correct_nested_methods = """
class A:
    def outer_method(self):
        def inner_method(self):
            super(A, self).ancestor()
"""


@pytest.mark.parametrize('code', [
    error_generator_expression,
    error_nested_comprehensions,
    error_multiple_nested_comprehensions,
    error_set_comprehension,
    error_list_comprehension,
    error_dict_comprehension,
    error_nested_methods,
])
def test_buggy_super_context(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that calling `super()` without args is caught."""
    tree = parse_ast_tree(code)

    visitor = BuggySuperCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [BuggySuperContextViolation])


@pytest.mark.parametrize('code', [
    correct_set_comprehension,
    correct_list_comprehension,
    correct_dict_comprehension,
    correct_generator_expression,
    correct_nested_methods,
])
def test_correct_super_context(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that calling `super()` without args is caught."""
    tree = parse_ast_tree(code)

    visitor = BuggySuperCallVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
