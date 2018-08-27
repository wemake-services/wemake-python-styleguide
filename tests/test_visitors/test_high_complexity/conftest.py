# -*- coding: utf-8 -*-

from collections import namedtuple

import pytest

from wemake_python_styleguide.options.defaults import (
    MAX_ARGUMENTS,
    MAX_EXPRESSIONS,
    MAX_LOCAL_VARIABLES,
    MAX_RETURNS,
)

Options = namedtuple('options', [
    'max_arguments',
    'max_expressions',
    'max_local_variables',
    'max_returns',
])

@pytest.fixture()
def options():
    """Returns the options builder."""
    def factory(**kwargs):
        defaults = {
            'max_arguments': MAX_ARGUMENTS,
            'max_expressions': MAX_EXPRESSIONS,
            'max_local_variables': MAX_LOCAL_VARIABLES,
            'max_returns': MAX_RETURNS,
        }

        defaults.update(kwargs)
        return Options(**defaults)

    return factory
