# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.base import ASTViolation


def test_visitor_returns_location():
    """Ensures that `BaseNodeVisitor` return correct violation message."""
    visitor = ASTViolation(node=ast.parse(''), text='violation')
    visitor.error_template = '{0}'
    visitor.code = 1
    assert visitor.node_items() == (0, 0, 'WPS001 violation')
