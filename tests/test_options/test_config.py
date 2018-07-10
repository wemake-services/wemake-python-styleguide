# -*- coding: utf-8 -*-

import subprocess


def test_max_variables_cli_option(absolute_path):
    """Test to check max-local-variables cli option."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_variables.py')
    option_flag = '--max-local-variables'
    option_value = '100'
    process = subprocess.Popen(
        ['flake8', filename, option_flag, option_value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(b'WPS150') == 0


def test_max_arguments_cli_option(absolute_path):
    """Test to check max-arguments cli option."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_arguments.py')
    option_flag = '--max-arguments'
    option_value = '100'
    process = subprocess.Popen(
        ['flake8', filename, option_flag, option_value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(b'WPS151') == 0


def test_max_returns_cli_option(absolute_path):
    """Test to check max-returns cli option."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_returns.py')
    option_flag = '--max-returns'
    option_value = '100'
    process = subprocess.Popen(
        ['flake8', filename, option_flag, option_value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(b'WPS153') == 0


def test_max_expressions_cli_options(absolute_path):
    """Test to check max-expressions cli option."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_expressions.py')
    option_flag = '--max-expressions'
    option_value = '100'
    process = subprocess.Popen(
        ['flake8', filename, option_flag, option_value],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert stdout.count(b'WPS154') == 0
