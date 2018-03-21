# -*- coding: utf-8 -*-

import subprocess


def test_base_rules_called_in_fixture(absolute_path):
    """End-to-End test to check complexity rules."""
    filename = absolute_path('fixtures', 'base_rules.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS001') == 1
    assert stdout.count(b'WPS002') == 2
