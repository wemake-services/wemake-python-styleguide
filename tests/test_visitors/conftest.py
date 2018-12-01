# -*- coding: utf-8 -*-

from typing import Sequence

import pytest

from wemake_python_styleguide.violations.base import (
    ASTViolation,
    TokenizeViolation,
)
from wemake_python_styleguide.visitors.base import BaseVisitor


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""
    def factory(visitor: BaseVisitor, errors: Sequence[str]):
        assert len(errors) == len(visitor.violations)

        for index, error in enumerate(visitor.violations):
            assert error.code == errors[index].code
            if isinstance(error, (ASTViolation, TokenizeViolation)):
                assert error._location() != (0, 0)  # noqa: Z441

    return factory


@pytest.fixture(scope='session')
def assert_error_text():
    """Helper function to assert visitor violation's text."""
    def factory(visitor: BaseVisitor, text: str):
        assert len(visitor.violations) == 1

        violation = visitor.violations[0]
        assert violation.__class__.should_use_text, violation.__class__

        reproduction = violation.__class__(
            node=violation._node,  # noqa: Z441
            text=text,
        )
        assert reproduction.message() == violation.message()  # noqa: S101

    return factory


@pytest.fixture()
def async_wrapper():
    """Fixture to convert all regular functions into async ones."""
    def factory(template: str) -> str:
        return template.replace(
            'def ', 'async def ',
        ).replace(
            'with ', 'async with ',
        ).replace(
            'for ', 'async for ',
        )
    return factory


@pytest.fixture()
def regular_wrapper():
    """Fixture to return regular functions without modifications."""
    def factory(template: str) -> str:
        return template
    return factory


@pytest.fixture(params=['async_wrapper', 'regular_wrapper'])
def mode(request):
    """Fixture that returns either `async` or regular functions."""
    return request.getfuncargvalue(request.param)
