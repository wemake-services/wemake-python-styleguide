# -*- coding: utf-8 -*-

from wemake_python_styleguide.options import config


def test_option_docs():
    """Ensures that all options are documented."""
    for option in config.Configuration._options:  # noqa: WPS437
        option_name = '``{0}``'.format(option.long_option_name[2:])
        assert option_name in config.__doc__


def test_option_help():
    """Ensures that all options has help."""
    for option in config.Configuration._options:  # noqa: WPS437
        assert len(option.help) > 10
        assert '%default' in option.help
        assert option.help.split(' Defaults to:')[0].endswith('.')
