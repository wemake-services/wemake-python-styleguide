# -*- coding: utf-8 -*-

import subprocess


def test_noqa_fixture_disabled(absolute_path):
    """End-to-End test to check that all violations are present."""
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
    output = stdout.decode('utf8')

    counts = {
        'Z110': 2,
        'Z111': 1,
        'Z112': 1,
        'Z113': 1,

        'Z220': 1,

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

        'Z410': 1,
        'Z420': 1,
        'Z421': 1,
        'Z422': 1,
        'Z423': 1,
        'Z430': 1,
        'Z431': 2,
        'Z432': 2,
        'Z433': 2,
        'Z434': 1,
        'Z435': 1,
        'Z436': 1,
    }

    for error in counts:
        # TODO: parse all `Z` error out, create a list
        # TODO: pop errors from `counts`, make sure nothing is left
        assert output.count(error) == counts[error], error


def test_noqa_fixture(absolute_path):
    """End-to-End test to check that `noqa` works."""
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', absolute_path('fixtures', 'noqa.py')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z') == 0
