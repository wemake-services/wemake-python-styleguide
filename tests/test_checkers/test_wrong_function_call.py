# -*- coding: utf-8 -*-

import subprocess


def test_wrong_function_called_in_fixture(absolute_path):
    filename = absolute_path('fixtures', 'wrong_function_call.py')
    p = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = p.communicate()

    assert stdout.count(b'WPS110') == 8
