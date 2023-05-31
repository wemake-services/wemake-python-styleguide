import pytest
from flake8 import __version_info__ as flake8_version_info
from flake8.options.manager import OptionManager

from wemake_python_styleguide import version
from wemake_python_styleguide.options import config


@pytest.fixture()
def option_parser():
    """Returns option parser that can be used for tests."""
    if flake8_version_info > (6, ):
        parser = OptionManager(
            version=version.pkg_version,
            plugin_versions='',
            parents=[],
            formatter_names=[],
        )
    elif flake8_version_info > (5, ):
        parser = OptionManager(
            version=version.pkg_version,
            plugin_versions='',
            parents=[],
        )
    else:
        parser = OptionManager(
            prog=version.pkg_name,
            version=version.pkg_version,
        )
    config.Configuration().register_options(parser)
    return parser
