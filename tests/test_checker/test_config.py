# -*- coding: utf-8 -*-

import subprocess

import pytest


@pytest.mark.parametrize('filename, option_flag, option_value, error_code', [
    ('wrong_arguments.py', '--max-arguments', '100', b'Z151'),
    ('async_wrong_arguments.py', '--max-arguments', '100', b'Z151'),
])
def test_max_variables_cli_option(
    absolute_path,
    filename,
    option_flag,
    option_value,
    error_code,
):
    """Test to check that cli options work."""
    fixture = absolute_path('fixtures', 'config', filename)
    process = subprocess.Popen(
        ['flake8', fixture, option_flag, option_value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(error_code) == 0
