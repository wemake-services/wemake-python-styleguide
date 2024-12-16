import pytest

from wemake_python_styleguide.violations.oop import (
    LambdaAttributeAssignedViolation,
)
from wemake_python_styleguide.visitors.ast.classes import ClassAttributeVisitor

# Correct:

correct_lambda_usage = """
class A:
    def method(self):
        return filter(lambda x: x - 1, items)
"""

# This might be an API or something:
correct_lambda_attr_assign1 = """
class A:
    def method(self, other):
        other.api = lambda x: x * 2
"""

correct_lambda_attr_assign2 = """
other.api = lambda x: x * 2
"""

correct_lambda_attr_assign3 = """
class A:
    other.api = lambda x: x * 2
"""

correct_lambda_attr_assign4 = """
def some(other):
    other.api = lambda x: x * 2
"""

# This is not strictly correct, but we won't detect this:
# TODO: maybe we should after we can create pairs of assigned values?
correct_lambda_attr_assign5 = """
class A:
    def __init__(self):
        self._api, self.other = (3, lambda x: x * 2)
"""

# Wrong:

wrong_lambda_assign1 = """
class A:
    def method(self, other):
        self.api = lambda x: x * 2
"""

wrong_lambda_assign2 = """
class A:
    def __init__(self):
        self._api = lambda x: x * 2
"""

wrong_lambda_assign3 = """
class A:
    @classmethod
    def build(cls):
        cls.__builder = lambda x: x * 2
"""

wrong_lambda_assign4 = """
class A:
    def __init__(self):
        self._api = temp = lambda x: x * 2
"""


@pytest.mark.parametrize(
    'code',
    [
        wrong_lambda_assign1,
        wrong_lambda_assign2,
        wrong_lambda_assign3,
        wrong_lambda_assign4,
    ],
)
def test_wrong_lambda_assign(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that wrong `lambda` assigns raise."""
    tree = parse_ast_tree(code)

    visitor = ClassAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [LambdaAttributeAssignedViolation])


@pytest.mark.parametrize(
    'code',
    [
        correct_lambda_attr_assign1,
        correct_lambda_attr_assign2,
        correct_lambda_attr_assign3,
        correct_lambda_attr_assign4,
        correct_lambda_attr_assign5,
    ],
)
def test_correct_lambda_assign(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that correct `lambda` assigns do not raise."""
    tree = parse_ast_tree(code)

    visitor = ClassAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
