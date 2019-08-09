# -*- coding: utf-8 -*-

from wemake_python_styleguide.options.config import Configuration


def test_option_docs():
    """Ensures that all options are documented."""
    for option in Configuration.options:
        option_name = '``{0}``'.format(option.long_option_name[2:])
        assert option_name in Configuration.__doc__


def test_option_help():
    """Ensures that all options has help."""
    for option in Configuration.options:
        assert len(option.help) > 10
        assert '%default' in option.help
        assert option.help.split(' Defaults to:')[0].endswith('.')
