# -*- coding: utf-8 -*-

import subprocess


def test_wrong_nested_in_fixture(absolute_path):
    """End-to-End test to check nested rules."""
    filename = absolute_path('fixtures', 'wrong_nested.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS140') == 2
    assert stdout.count(b'WPS141') == 2
