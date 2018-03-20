# -*- coding: utf-8 -*-

import subprocess


def test_wrong_imports_in_fixture(absolute_path):
    """End-to-End test to check import rules."""
    filename = absolute_path('fixtures', 'wrong_import.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS130') == 4
    assert stdout.count(b'WPS131') == 2
    assert stdout.count(b'WPS132') == 1
