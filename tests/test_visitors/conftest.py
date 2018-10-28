# -*- coding: utf-8 -*-

from typing import Sequence

import pytest

from wemake_python_styleguide.visitors.base import BaseVisitor


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""
    def factory(visitor: BaseVisitor, errors: Sequence[str]):
        assert len(errors) == len(visitor.violations)

        for index, error in enumerate(visitor.violations):
            assert error.code == errors[index].code

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
        assert reproduction.message() == violation.message()

    return factory
