import ast
import re

import pytest

from wemake_python_styleguide.violations.base import ASTViolation


class NewViolation(ASTViolation):
    """
    Yells at cloud.

    Yay, I'm a docstring!
    """

    code = 1
    error_template = '{0}'


def test_visitor_returns_location():
    """Ensures that `BaseNodeVisitor` return correct violation message."""
    assert NewViolation.full_code == 'WPS001'
    assert NewViolation.summary == 'Yells at cloud.'

    visitor = NewViolation(node=ast.parse(''), text='violation')
    assert visitor.node_items() == (0, 0, 'WPS001 violation')


def test_violation_must_have_docstring():
    """Ensures that `BaseNodeVisitor` return correct violation message."""
    with pytest.raises(
        TypeError,
        match=re.escape(
            'Please include a docstring documenting ' +
            "<class 'test_implementation.test_violation_must_have_docstring." +
            "<locals>.IShallNotPass'>",
        ),
    ):

        class IShallNotPass(ASTViolation):  # noqa: WPS431
            code = 123
