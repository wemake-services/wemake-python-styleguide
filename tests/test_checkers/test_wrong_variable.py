# -*- coding: utf-8 -*-

import subprocess


def test_wrong_variables_in_fixture(absolute_path):
    """End-to-End test to check variable rules."""
    filename = absolute_path('fixtures', 'wrong_variable.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z114') == 12
    assert stdout.count(b'Z115') == 6
    assert stdout.count(b'Z116') == 1
    assert stdout.count(b'Z117') == 1
