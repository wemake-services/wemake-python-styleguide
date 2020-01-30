# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    WrongMethodOrderViolation,
)
from wemake_python_styleguide.visitors.ast.classes import (
    ClassMethodOrderVisitor,
)

correct_method_order = """
class Test(object):
    def __new__(self):
        ...

    def __init__(self):
        ...

    def __call__(self):
        ...

    def public(self):
        ...

    def __bool__(self):
        ...

    def public1(self):
        ...

    def _protected(self):
        ...

    def _mixed(self):
        ...

    def __private(self):
        ...

    def __private2(self):
        ...
"""

nested_functions = """
class Test(object):
    def _protected(self):
        def factory():
            ...
        ...
"""

class_template = """
class Template(object):
    def {0}(self):
        ...

    def {1}(self):
        ...
"""


@pytest.mark.parametrize('code', [
    correct_method_order,
    nested_functions,
])
def test_correct_method_order(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
):
    """Testing that correct method order is allowed."""
    tree = parse_ast_tree(mode(code))

    visitor = ClassMethodOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('first', 'second'), [
    ('__init__', '__new__'),
    ('__call__', '__init__'),
    ('__call__', '__new__'),

    ('public', '__new__'),
    ('public', '__init__'),
    ('public', '__call__'),
    ('__magic__', '__new__'),
    ('__magic__', '__init__'),
    ('__magic__', '__call__'),

    ('_protected', '__new__'),
    ('_protected', '__init__'),
    ('_protected', '__call__'),
    ('_protected', 'public'),
    ('_protected', '__magic__'),

    ('__private', '__new__'),
    ('__private', '__init__'),
    ('__private', '__call__'),
    ('__private', 'public'),
    ('__private', '__magic__'),
    ('__private', '_protected'),
])
def test_incorrect_method_order(
    assert_errors,
    parse_ast_tree,
    default_options,
    first,
    second,
    mode,
):
    """Testing that incorrect method order is prohibited."""
    tree = parse_ast_tree(mode(class_template.format(first, second)))

    visitor = ClassMethodOrderVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [WrongMethodOrderViolation])
