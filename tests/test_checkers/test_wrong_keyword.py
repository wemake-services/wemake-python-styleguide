# -*- coding: utf-8 -*-

import subprocess


def test_wrong_keyword_in_fixture(absolute_path):
    """End-to-End test to check keyword rules."""
    filename = absolute_path('fixtures', 'wrong_keyword.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS100') == 5
