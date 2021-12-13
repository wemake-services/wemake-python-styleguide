import pytest

from wemake_python_styleguide.violations.oop import (
    WrongClassBodyContentViolation,
)
from wemake_python_styleguide.visitors.ast.classes import WrongClassBodyVisitor

class_body_template = """
class ClassWithBody(object):
    {0}
"""


@pytest.mark.parametrize('code', [
    '...',
    '1',
    'None',
    'False',
    'call()',
    'for index in range(10):\n       index = index + 1',
    'if some_value:\n        index = 1',
    'while True:\n        index = 1',
])
def test_incorrect_body_items(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that incorrect body nodes are prohibited."""
    tree = parse_ast_tree(class_body_template.format(code))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongClassBodyContentViolation])


@pytest.mark.parametrize('code', [
    '"""Docstring."""',
    'some_value = 3',
    'some_value = True if some_other else default',
    'some_value: int',
    'def method(self, arg: int): ...',
    'def method(self, arg): ...',
    'def method(self, arg: int) -> None: ...',
    'class Meta(object):\n        """Docs."""',
])
def test_body_correct_items(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
    mode,
):
    """Testing correct body items are allowed."""
    tree = parse_ast_tree(mode(class_body_template.format(code)))

    visitor = WrongClassBodyVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
