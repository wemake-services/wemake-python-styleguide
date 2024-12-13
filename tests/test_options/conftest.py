import pytest
from flake8.options.manager import OptionManager

from wemake_python_styleguide import version
from wemake_python_styleguide.options import config


@pytest.fixture
def option_parser():
    """Returns option parser that can be used for tests."""
    parser = OptionManager(
        version=version.pkg_version,
        plugin_versions='',
        parents=[],
        formatter_names=[],
    )
    config.Configuration().register_options(parser)
    return parser
