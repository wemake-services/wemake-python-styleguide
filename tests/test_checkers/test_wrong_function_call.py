# -*- coding: utf-8 -*-

import subprocess


def test_wrong_function_called_in_fixture(absolute_path):
    """End-to-End test to check function call rules."""
    filename = absolute_path('fixtures', 'wrong_function_call.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS110') == 10
