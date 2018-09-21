# -*- coding: utf-8 -*-

from wemake_python_styleguide.errors.base import BaseStyleViolation


def test_checker_default_location():
    """Ensures that `BaseStyleViolation` returns correct location."""
    assert BaseStyleViolation(None)._location() == (0, 0)


def test_all_unique_error_codes(all_errors):
    """Ensures that all errors have unique error codes."""
    codes = []
    for error in all_errors:
        codes.append(int(error.code))

    assert len(set(codes)) == len(all_errors)


def test_all_errors_have_description_with_code(all_errors):
    """Ensures that all errors have description with error code."""
    for error in all_errors:
        assert str(error.code) in error.__doc__
