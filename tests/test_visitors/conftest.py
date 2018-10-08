# -*- coding: utf-8 -*-

from collections import namedtuple
from typing import Sequence

import pytest

from wemake_python_styleguide.options.config import Configuration
from wemake_python_styleguide.visitors.base import BaseVisitor


def _to_dest_option(long_option_name: str) -> str:
    return long_option_name[2:].replace('-', '_')


@pytest.fixture(scope='session')
def assert_errors():
    """Helper function to assert visitor violations."""
    def factory(visitor: BaseVisitor, errors: Sequence[str]):
        for index, error in enumerate(visitor.violations):
            assert len(errors) > index, [
                (type(error), error.message()) for error in visitor.violations
            ]
            assert error.code == errors[index].code

        assert len(visitor.violations) == len(errors)

    return factory


@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    default_values = {
        _to_dest_option(option.long_option_name): option.default
        for option in Configuration.options
    }

    Options = namedtuple('options', default_values.keys())

    def factory(**kwargs):
        final_options = default_values.copy()
        final_options.update(kwargs)
        return Options(**final_options)

    return factory


@pytest.fixture(scope='session')
def default_options(options):
    """Returns the default options."""
    return options()
