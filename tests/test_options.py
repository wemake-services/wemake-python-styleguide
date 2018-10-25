# -*- coding: utf-8 -*-

from wemake_python_styleguide.options.config import Configuration


def test_option_docs():
    """Ensures that all options are documented."""
    for option in Configuration.options:
        option_name = '``' + option.long_option_name[2:] + '``'
        assert option_name in Configuration.__doc__
