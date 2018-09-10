# -*- coding: utf-8 -*-

import subprocess


def test_regression_122(absolute_path):
    """
    For some reason there was an issue with `compat.py`.

    When installing this package via `pip` there was an issue with
    `ast` parsing. But, after moving `compat.py` to tests only,
    the issue seems to be gone.

    Conclusion: do not touch something that is working!

    See: https://github.com/wemake-services/wemake-python-styleguide/issues/112
    """
    fixture = absolute_path('fixtures', 'regression', 'issue112.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', fixture],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z') == 0
