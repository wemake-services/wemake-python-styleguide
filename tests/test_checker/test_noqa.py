# -*- coding: utf-8 -*-

import re
import subprocess
from collections import Counter

ERROR_PATTERN = re.compile(r'(Z\d{3})')


def _assert_errors_count_in_output(output, errors):
    found_errors = Counter((
        match.group(0) for match in ERROR_PATTERN.finditer(output)
    ))

    for found_error, found_count in found_errors.items():
        assert found_error in errors, 'Error without a noqa count'
        assert found_count == errors.pop(found_error)
    assert len(errors) == 0


def test_noqa_fixture_disabled(absolute_path):
    """End-to-End test to check that all violations are present."""
    errors = {
        'Z110': 2,
        'Z111': 1,
        'Z112': 1,
        'Z113': 1,
        'Z114': 1,
        'Z115': 1,
        'Z116': 1,

        'Z220': 1,
        'Z224': 1,

        'Z300': 1,
        'Z302': 1,
        'Z303': 1,
        'Z304': 1,
        'Z305': 1,
        'Z306': 2,
        'Z307': 1,
        'Z308': 1,
        'Z309': 1,
        'Z310': 4,
        'Z311': 1,
        'Z312': 1,
        'Z313': 1,
        'Z314': 1,
        'Z315': 1,

        'Z410': 1,
        'Z420': 1,
        'Z421': 1,
        'Z422': 1,
        'Z423': 1,
        'Z424': 1,
        'Z430': 1,
        'Z431': 2,
        'Z432': 2,
        'Z433': 2,
        'Z434': 1,
        'Z435': 1,
        'Z436': 1,
        'Z437': 1,
        'Z438': 1,
        'Z439': 1,
        'Z440': 1,
        'Z441': 1,
    }

    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--select',
            'Z',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    _assert_errors_count_in_output(stdout.decode('utf8'), errors)


def test_noqa_fixture(absolute_path):
    """End-to-End test to check that `noqa` works."""
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', absolute_path('fixtures', 'noqa.py')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z') == 0
