import pytest
from flake8.options.manager import OptionManager

from wemake_python_styleguide import version
from wemake_python_styleguide.options import config


@pytest.fixture()
def option_parser():
    """Returns option parser that can be used for tests."""
    parser = OptionManager(
        prog=version.pkg_name,
        version=version.pkg_version,
    )
    config.Configuration().register_options(parser)
    return parser
