# -*- coding: utf-8 -*-

from wemake_python_styleguide.config import ConfigFileParser


def test_config_parsing(absolute_path):
    """Test to check that config parsing is correct."""
    filename = absolute_path('fixtures', 'setup.cfg')
    config_parser = ConfigFileParser(filename)
    some_option = config_parser.get_option('some-option')
    assert some_option == 1
