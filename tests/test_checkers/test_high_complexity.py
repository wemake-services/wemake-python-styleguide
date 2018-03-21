# -*- coding: utf-8 -*-

import subprocess


def test_high_complexity_called_in_fixture(absolute_path):
    """End-to-End test to check complexity rules."""
    filename = absolute_path('fixtures', 'high_complexity.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS150') == 2
    assert stdout.count(b'WPS151') == 4
    assert stdout.count(b'WPS153') == 1
