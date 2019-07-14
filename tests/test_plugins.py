# -*- coding: utf-8 -*-

"""
These test ensures that each plugin is enabled and working.

We only test a single warning from each plugin.
We do not test that any of the 3rd party plugins work correctly.

It is not our responsibility.
"""


import subprocess


def _assert_plugin_output(output):
    assert output.count('A001') > 0  # flake8-builtins
    assert output.count('B002') > 0  # flake8-bugbear
    assert output.count('C101') > 0  # flake8-coding
    assert output.count('C400') > 0  # flake8-comprehensions
    assert output.count('C819') > 0  # flake8-commas
    assert output.count('D103') > 0  # flake8-docstring
    assert output.count('E225') > 0  # pycodestyle
    assert output.count('E800') > 0  # flake8-eradicate
    assert output.count('F401') > 0  # flake8
    assert output.count('G001') > 0  # flake8-logging-format
    assert output.count('I001') > 0  # flake8-isort
    assert output.count('N400') > 0  # flake8-broken-line
    assert output.count('N802') > 0  # pep8-naming
    assert output.count('P101') > 0  # flake8-string-format
    assert output.count('Q000') > 0  # flake8-quotes
    assert output.count('Q003') > 0  # flake8-quotes
    assert output.count('S001') > 0  # flake8-pep3101
    assert output.count('S101') > 0  # flake8-bandit
    assert output.count('T001') > 0  # flake8-print
    assert output.count('T100') > 0  # flake8-debugger
    assert output.count('TAE002') > 0  # flake8-annotations-complexity
    assert output.count('RST299') > 0  # flake8-rst-docstrings
    assert output.count('EXE003') > 0  # flake8-executable


def test_external_plugins(absolute_path):
    """End-to-End test to check that all plugins are enabled."""
    filename = absolute_path('fixtures', 'external_plugins.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--enable-extensions',
            'G',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    _assert_plugin_output(output)


def test_external_plugins_diff(absolute_path):
    """Ensures that our linter and all plugins work in ``diff`` mode."""
    process = subprocess.Popen(
        [
            'diff',
            '-uN',  # is required to ignore missing files
            'missing_file',  # is required to transform file to diff
            absolute_path('fixtures', 'external_plugins.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )

    output = subprocess.check_output(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--enable-extensions',
            'G',
            '--diff',  # is required to test diffs! ;)
            '--exit-zero',  # to allow failures
        ],
        stdin=process.stdout,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    process.wait()

    _assert_plugin_output(output)
