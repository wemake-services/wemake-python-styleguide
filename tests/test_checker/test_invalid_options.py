# -*- coding: utf-8 -*-

import subprocess


def test_invalid_options(absolute_path):
    """End-to-End test to check option validation works."""
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            '--max-imports',
            '-5',  # should be positive
            'Z',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    process.communicate()

    assert process.returncode == 2
