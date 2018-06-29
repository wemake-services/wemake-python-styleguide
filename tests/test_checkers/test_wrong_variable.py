# -*- coding: utf-8 -*-

import subprocess


def test_wrong_variables_in_fixture(absolute_path):
    """End-to-End test to check variable rules."""
    filename = absolute_path('fixtures', 'wrong_variable.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS120') == 8
    assert stdout.count(b'WPS121') == 3
    assert stdout.count(b'WPS122') == 3
    assert stdout.count(b'WPS123') == 2
    assert stdout.count(b'WPS124') == 1
    assert stdout.count(b'WPS125') == 1
    assert stdout.count(b'WPS126') == 1
