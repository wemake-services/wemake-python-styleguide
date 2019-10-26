# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    MutableClassAttributesViolation,
)
from wemake_python_styleguide.visitors.ast.classes import (
    ClassMutableAttributeVisitor,
)

class_template = """
class ClassWithAttr(object):
    field = {0}
"""

mutable_assign = (
    '[]',
    '{"key": value}',
    'list()',
    'dict()',
)

immutable_assign = (
    '0',
    'False',
    'None',
    '0.0',
    'tuple()',
)


@pytest.mark.parametrize('code', mutable_assign)
def test_mutable_attributes(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Testing that mutable attributes are forbidden."""
    tree = parse_ast_tree(class_template.format(code))

    visitor = ClassMutableAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [MutableClassAttributesViolation])


@pytest.mark.parametrize('code', immutable_assign)
def test_immutable_attributes(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
):
    """Ensure that immutable attributes are allowed."""
    tree = parse_ast_tree(class_template.format(code))

    visitor = ClassMutableAttributeVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
