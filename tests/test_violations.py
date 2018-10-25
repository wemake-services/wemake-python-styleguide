# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.base import ASTViolation, BaseViolation


def test_visitor_returns_location():
    """Ensures that `BaseNodeVisitor` return correct violation message."""
    visitor = ASTViolation(node=ast.parse(''), text='violation')
    visitor.error_template = '{0}'
    visitor.code = 1
    assert visitor.node_items() == (0, 0, 'Z001 violation')


def test_all_violations_correct_numbers(all_module_violations):
    """Ensures that all violations has correct violation code numbers."""
    assert len(all_module_violations) == 4

    for index, module in enumerate(all_module_violations.keys()):
        classes = all_module_violations[module]
        code_number = (index + 1) * 100
        for violation_class in classes:
            assert code_number <= violation_class.code <= code_number + 100 - 1


def test_all_violations_are_documented(all_module_violations):
    """Ensures that all violations are documented."""
    for module, classes in all_module_violations.items():
        for violation_class in classes:
            # Once per `summary` and once per `autoclass`:
            assert module.__doc__.count(violation_class.__qualname__) == 2


def test_checker_default_location():
    """Ensures that `BaseViolation` returns correct location."""
    assert BaseViolation(None)._location() == (0, 0)


def test_all_unique_violation_codes(all_violations):
    """Ensures that all violations have unique violation codes."""
    codes = []
    for violation in all_violations:
        codes.append(int(violation.code))

    assert len(set(codes)) == len(all_violations)


def test_all_violations_have_description_with_code(all_violations):
    """Ensures that all violations have description with violation code."""
    for violation in all_violations:
        assert str(violation.code) in violation.__doc__


def test_all_violations_have_versionadded(all_violations):
    """Ensures that all violations have `versionadded` tag."""
    for violation in all_violations:
        assert '.. versionadded:: ' in violation.__doc__
