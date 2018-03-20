# -*- coding: utf-8 -*-

import subprocess


def test_wrong_variables_in_fixture(absolute_path):
    filename = absolute_path('fixtures', 'wrong_variable.py')
    p = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert stdout.count(b'WPS120') == 6
    assert stdout.count(b'WPS121') == 2
    assert stdout.count(b'WPS122') == 2
    assert stdout.count(b'WPS123') == 1
    assert stdout.count(b'WPS124') == 1
