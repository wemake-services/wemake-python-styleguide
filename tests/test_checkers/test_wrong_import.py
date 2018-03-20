# -*- coding: utf-8 -*-

import subprocess


def test_wrong_imports_in_fixture(absolute_path):
    filename = absolute_path('fixtures', 'wrong_import.py')
    p = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert stdout.count(b'WPS130') == 4
    assert stdout.count(b'WPS131') == 2
    assert stdout.count(b'WPS132') == 1
