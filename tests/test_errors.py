# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.errors.base import (
    ASTStyleViolation,
    BaseStyleViolation,
)


def test_visitor_returns_location():
    """Ensures that `BaseNodeVisitor` return correct error message."""
    visitor = ASTStyleViolation(node=ast.parse(''), text='error')
    visitor.error_template = '{0}'
    visitor.code = 1
    assert visitor.node_items() == (0, 0, 'Z001 error')


def test_all_errors_correct_numbers(all_module_errors):
    """Ensures that all violations has correct error code numbers."""
    assert len(all_module_errors) == 4

    for index, module in enumerate(all_module_errors.keys()):
        classes = all_module_errors[module]
        code_number = (index + 1) * 100
        for error_class in classes:
            assert code_number <= error_class.code <= code_number + 100 - 1


def test_all_errors_are_documented(all_module_errors):
    """Ensures that all violations are documented."""
    for module, classes in all_module_errors.items():
        for error_class in classes:
            # Once per summary and once per autoclass:
            assert module.__doc__.count(error_class.__qualname__) == 2


def test_checker_default_location():
    """Ensures that `BaseStyleViolation` returns correct location."""
    assert BaseStyleViolation(None)._location() == (0, 0)


def test_all_unique_error_codes(all_errors):
    """Ensures that all violations have unique error codes."""
    codes = []
    for error in all_errors:
        codes.append(int(error.code))

    assert len(set(codes)) == len(all_errors)


def test_all_errors_have_description_with_code(all_errors):
    """Ensures that all violations have description with error code."""
    for error in all_errors:
        assert str(error.code) in error.__doc__
