import os
from collections import namedtuple

import pytest

from wemake_python_styleguide.options.config import Configuration

pytest_plugins = [
    'plugins.violations',
    'plugins.ast_tree',
    'plugins.tokenize_parser',
    'plugins.async_sync',
]


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files: str):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, *files)
    return factory


@pytest.fixture(scope='session')
def options():
    """Returns the options builder."""
    default_values = {
        option.long_option_name[2:].replace('-', '_'): option.default
        for option in Configuration._options  # noqa: WPS437
    }

    Options = namedtuple('options', default_values.keys())

    def factory(**kwargs):
        final_options = default_values.copy()
        final_options.update(kwargs)
        return Options(**final_options)

    return factory


@pytest.fixture(scope='session')
def default_options(options):  # noqa: WPS442
    """Returns the default options."""
    return options()
