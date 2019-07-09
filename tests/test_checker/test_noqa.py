# -*- coding: utf-8 -*-

import re
import subprocess
from collections import Counter

ERROR_PATTERN = re.compile(r'(Z\d{3})')
IGNORED_VIOLATIONS = (
    'Z202',  # since our test case is complex, that's fine
    'Z226',  # we have a lot of ugly strings inside,
    'Z402',  # since we obviously use a lot of `noqa` comments
)


def _assert_errors_count_in_output(output, errors, all_violations):
    found_errors = Counter((
        match.group(0) for match in ERROR_PATTERN.finditer(output)
    ))

    for violation in all_violations:
        key = 'Z' + str(violation.code).zfill(3)
        assert key in errors, 'Unlisted #noqa violation'

    for found_error, found_count in found_errors.items():
        assert found_error in errors, 'Violation without a #noqa count'
        assert found_count == errors.pop(found_error)

    assert list(filter(
        lambda key: errors[key] != 0,
        errors,
    )) == []


def test_noqa_fixture_disabled(absolute_path, all_violations):
    """End-to-End test to check that all violations are present."""
    errors = {
        'Z100': 0,
        'Z101': 0,
        'Z102': 0,

        'Z110': 3,
        'Z111': 1,
        'Z112': 1,
        'Z113': 1,
        'Z114': 1,
        'Z115': 1,
        'Z116': 1,
        'Z117': 1,
        'Z118': 1,
        'Z119': 1,
        'Z120': 1,
        'Z121': 1,

        'Z200': 0,
        'Z201': 0,
        'Z202': 0,

        'Z210': 1,
        'Z211': 1,
        'Z212': 1,
        'Z213': 1,
        'Z214': 0,
        'Z215': 1,
        'Z216': 0,
        'Z217': 1,

        'Z220': 1,
        'Z221': 2,
        'Z222': 1,
        'Z223': 1,
        'Z224': 1,
        'Z225': 1,
        'Z226': 0,
        'Z227': 1,

        'Z300': 1,
        'Z301': 1,
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
        'Z316': 0,
        'Z317': 1,
        'Z318': 3,
        'Z319': 2,
        'Z320': 2,
        'Z321': 1,
        'Z322': 1,
        'Z323': 0,
        'Z324': 1,
        'Z325': 1,
        'Z326': 1,
        'Z327': 1,
        'Z328': 2,
        'Z329': 1,
        'Z330': 1,
        'Z331': 1,

        'Z400': 0,
        'Z401': 0,
        'Z402': 0,
        'Z403': 0,

        'Z410': 1,
        'Z411': 0,
        'Z412': 0,
        'Z413': 1,

        'Z420': 2,
        'Z421': 1,
        'Z422': 1,
        'Z423': 1,
        'Z424': 1,
        'Z425': 1,
        'Z426': 1,

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
        'Z442': 1,
        'Z443': 1,
        'Z444': 2,
        'Z445': 1,
        'Z446': 1,
        'Z447': 1,
        'Z448': 1,
        'Z449': 1,
        'Z450': 1,
        'Z451': 2,
        'Z452': 2,
        'Z453': 1,
        'Z454': 1,
        'Z455': 1,
        'Z456': 1,
        'Z457': 1,
        'Z458': 1,
        'Z459': 1,
        'Z460': 1,
        'Z461': 1,
        'Z462': 1,
        'Z463': 1,
        'Z464': 1,
        'Z465': 1,
        'Z466': 1,
        'Z467': 1,
        'Z468': 1,
        'Z469': 1,
        'Z470': 1,
        'Z471': 1,
    }

    process = subprocess.Popen(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--disable-noqa',
            '--isolated',
            '--select',
            'Z',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    _assert_errors_count_in_output(
        stdout, errors, all_violations,
    )


def test_noqa_fixture(absolute_path):
    """End-to-End test to check that `noqa` works."""
    process = subprocess.Popen(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--isolated',
            '--select',
            'Z',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    assert stdout.count('Z') == 0


def test_noqa_fixture_without_ignore(absolute_path):
    """End-to-End test to check that `noqa` works without ignores."""
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'Z',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    for violation in IGNORED_VIOLATIONS:
        assert stdout.count(violation) > 0
