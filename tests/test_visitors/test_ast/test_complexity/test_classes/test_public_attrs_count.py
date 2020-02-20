# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyPublicAttributesViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.classes import (
    ClassComplexityVisitor,
)

class_template = """
class Test(object):
    def __init__(self):
        {0}

    def other(self):
        {1}
"""

module_template = """
{0}
{1}
"""

function_template = """
def some():
    {0}
    {1}
"""


@pytest.mark.parametrize('code', [
    class_template,
    module_template,
    function_template,
])
@pytest.mark.parametrize('expression', [
    'print()',
    'print(self)',
    'print(self.attr)',
    'print(self.attr.diff)',
    'self.attr.diff = 1',
    'self.attr.diff()',
    'some.attr = 1',
    'some.self = 1',
    'self = 1',
    'self[0] = 1',
    'self._protected = 1',
    'self.__private = 1',
    'self._protected = self.public',
    'cls.public = 1',
    'mcs.public = 1',
])
def test_correct_attributes(
    assert_errors,
    parse_ast_tree,
    code,
    expression,
    options,
    mode,
):
    """Testing of correct base classes number."""
    tree = parse_ast_tree(mode(code.format(expression, expression)))

    option_values = options(max_attributes=1)
    visitor = ClassComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    class_template,
])
@pytest.mark.parametrize(('expression1', 'expression2'), [
    ('self.public = 1', 'self.other = 1'),
    ('self.public = self.other', 'self.other = 1'),
    ('self.public = self.other', 'self.other = self.public'),
])
def test_wrong_attributes_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    expression1,
    expression2,
    options,
    mode,
):
    """Testing of correct base classes number."""
    tree = parse_ast_tree(mode(code.format(expression1, expression2)))

    option_values = options(max_attributes=1)
    visitor = ClassComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyPublicAttributesViolation])
    assert_error_text(visitor, '2', option_values.max_attributes)


@pytest.mark.parametrize('code', [
    module_template,
    function_template,
])
@pytest.mark.parametrize('expression', [
    'self.public = 1',
    'self.public: int = 1',
    'self.public = self.other',
])
def test_attributes_outside_class(
    assert_errors,
    parse_ast_tree,
    code,
    expression,
    options,
    mode,
):
    """Testing of correct base classes number."""
    tree = parse_ast_tree(mode(code.format(expression, expression)))

    option_values = options(max_attributes=1)
    visitor = ClassComplexityVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
