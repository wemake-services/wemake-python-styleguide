import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantEnumerateViolation,
)
from wemake_python_styleguide.visitors.ast.redundancy import (
    RedundantEnumerateVisitor,
)

# Correct:

correct_iteration_without_enumerate = """
def container():
    for item in items:
      ...
"""

correct_iteration_without_enumerate_raw = """
def container():
    for item in (1, 2, 3):
      ...
"""

correct_iteration_enumerate_receiver = """
def container():
    for result in enumerate(items):
      ...
"""

correct_iteration_enumerate_tuple = """
def container():
    for i, value in enumerate(items):
      ...
"""

correct_iteration_enumerate_comprehension = """
def container():
    some_value = {
        something
        for index, something in enumerate(items)
    }
"""

correct_iteration_anonymous_func = """
def container():
    for item in (lambda a: [a])(42):
      ...
"""

# Wrong:

wrong_iteration_enumerate_tuple_placeholder = """
def container():
    for _, item in enumerate(items):
      ...
"""

wrong_iteration_with_receiver_placeholder = """
def container():
    for _ in enumerate(items):
        ...
"""

wrong_iteration_set_comprehension = """
def container():
    some_value = {
        something
        for _, something in enumerate(items)
    }
"""

wrong_iteration_dict_comprehension = """
def container():
    some_value = {
        something: something
        for _, something in enumerate(items)
    }
"""

wrong_iteration_generator_expression = """
def container():
    some_value = (
        something
        for _, something in enumerate(items)
    )
"""

wrong_iteration_multiple_generators = """
def container():
    some_value = (
        something
        for _, something in enumerate(items)
        for i, v in enumerate([1, 2, 3])
        for _, another in enumerate(stuff)
    )
"""


@pytest.mark.parametrize('code', [
    wrong_iteration_enumerate_tuple_placeholder,
    wrong_iteration_with_receiver_placeholder,
    wrong_iteration_set_comprehension,
    wrong_iteration_dict_comprehension,
    wrong_iteration_generator_expression,
])
def test_wrong_usage_of_enumerate(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect return annotations is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = RedundantEnumerateVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantEnumerateViolation])


@pytest.mark.parametrize('code', [
    wrong_iteration_multiple_generators,
])
def test_wrong_multiple_generators(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that using incorrect return annotations is forbidden."""
    tree = parse_ast_tree(mode(code))

    visitor = RedundantEnumerateVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [
        RedundantEnumerateViolation,
        RedundantEnumerateViolation,
    ])


@pytest.mark.parametrize('code', [
    correct_iteration_without_enumerate,
    correct_iteration_without_enumerate_raw,
    correct_iteration_anonymous_func,
    correct_iteration_enumerate_receiver,
    correct_iteration_enumerate_tuple,
    correct_iteration_enumerate_comprehension,
])
def test_correct_usage_of_enumerate(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Ensures that it is possible to use correct type annotations."""
    tree = parse_ast_tree(mode(code))

    visitor = RedundantEnumerateVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
