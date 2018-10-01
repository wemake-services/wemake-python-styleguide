# -*- coding: utf-8 -*-

import subprocess


def test_noqa_fixture_disabled(absolute_path):
    """End-to-End test to check that all violations are present."""
    filename = absolute_path('fixtures', 'noqa.py')
    process = subprocess.Popen(
        ['flake8', '--disable-noqa', '--select', 'Z', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z') > 0


def test_noqa_fixture(absolute_path):
    """End-to-End test to check that `noqa` works."""
    filename = absolute_path('fixtures', 'noqa.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z') == 0
