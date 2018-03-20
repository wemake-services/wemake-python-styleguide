# -*- coding: utf-8 -*-

import subprocess


def test_wrong_keyword_in_fixture(absolute_path):
    filename = absolute_path('fixtures', 'wrong_keyword.py')
    p = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert stdout.count(b'WPS100') == 5
