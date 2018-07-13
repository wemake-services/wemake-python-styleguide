# -*- coding: utf-8 -*-

import inspect
from operator import itemgetter

import pytest

from wemake_python_styleguide import errors


def _is_error_class(cls) -> bool:
    return (
        inspect.isclass(cls) and
        issubclass(cls, errors.BaseStyleViolation) and
        cls is not errors.BaseStyleViolation
    )


@pytest.fixture(scope='module')
def all_errors():
    """Loads all errors from the package."""
    return list(
        map(itemgetter(1), inspect.getmembers(errors, _is_error_class)),
    )


def test_all_unique_error_codes(all_errors):
    """Ensures that all errors have unique error codes."""
    codes = []
    for error in all_errors:
        codes.append(error._code)

    assert len(set(codes)) == len(all_errors)


def test_all_errors_have_description_with_code(all_errors):
    """Ensures that all errors have description with error code."""
    for error in all_errors:
        assert error._code in error.__doc__
