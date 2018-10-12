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
