# -*- coding: utf-8 -*-

"""
Integration tests definition.

These are integration tests for several things:

1. that violation is active and enabled
2. that violation is raised for the bad code
3. that line number where violation is raised is correct
4. that `noqa` works

Docs: https://wemake-python-stylegui.de/en/latest/pages/api/contributing.html
"""

import re
import subprocess
import types
from collections import Counter

ERROR_PATTERN = re.compile(r'(WPS\d{3})')
IGNORED_VIOLATIONS = (
    'WPS202',  # since our test case is complex, that's fine
    'WPS204',  # our tests have a lot of overused expressions
    'WPS226',  # we have a lot of ugly strings inside,
    'WPS402',  # since we obviously use a lot of `noqa` comments
)

SHOULD_BE_RAISED = types.MappingProxyType({
    'WPS100': 0,
    'WPS101': 0,
    'WPS102': 0,
    'WPS110': 3,
    'WPS111': 1,
    'WPS112': 1,
    'WPS113': 1,
    'WPS114': 1,
    'WPS115': 1,
    'WPS116': 1,
    'WPS117': 1,
    'WPS118': 1,
    'WPS119': 1,
    'WPS120': 1,
    'WPS121': 1,
    'WPS122': 1,
    'WPS123': 1,

    'WPS200': 0,
    'WPS201': 0,
    'WPS202': 0,
    'WPS203': 0,
    'WPS204': 0,

    'WPS210': 1,
    'WPS211': 1,
    'WPS212': 1,
    'WPS213': 1,
    'WPS214': 0,
    'WPS215': 1,
    'WPS216': 0,
    'WPS217': 1,
    'WPS218': 1,
    'WPS219': 1,
    'WPS220': 1,
    'WPS221': 2,
    'WPS222': 1,
    'WPS223': 1,
    'WPS224': 1,
    'WPS225': 1,
    'WPS226': 0,
    'WPS227': 1,
    'WPS228': 1,
    'WPS229': 1,
    'WPS230': 1,

    'WPS300': 1,
    'WPS301': 1,
    'WPS302': 1,
    'WPS303': 1,
    'WPS304': 1,
    'WPS305': 1,
    'WPS306': 2,
    'WPS307': 1,
    'WPS308': 1,
    'WPS309': 1,
    'WPS310': 4,
    'WPS311': 1,
    'WPS312': 1,
    'WPS313': 1,
    'WPS314': 1,
    'WPS315': 1,
    'WPS316': 0,
    'WPS317': 1,
    'WPS318': 3,
    'WPS319': 2,
    'WPS320': 2,
    'WPS321': 1,
    'WPS322': 1,
    'WPS323': 0,
    'WPS324': 1,
    'WPS325': 1,
    'WPS326': 1,
    'WPS327': 1,
    'WPS328': 2,
    'WPS329': 1,
    'WPS330': 1,
    'WPS331': 1,
    'WPS332': 1,
    'WPS333': 1,
    'WPS334': 1,
    'WPS335': 1,
    'WPS336': 1,
    'WPS337': 1,
    'WPS338': 1,
    'WPS339': 1,
    'WPS340': 1,
    'WPS341': 1,
    'WPS342': 1,
    'WPS343': 1,
    'WPS344': 1,
    'WPS345': 1,
    'WPS346': 1,
    'WPS347': 3,

    'WPS400': 0,
    'WPS401': 0,
    'WPS402': 0,
    'WPS403': 0,
    'WPS404': 1,
    'WPS405': 1,
    'WPS406': 1,
    'WPS407': 1,
    'WPS408': 1,
    'WPS409': 1,
    'WPS410': 1,
    'WPS411': 0,
    'WPS412': 0,
    'WPS413': 1,
    'WPS414': 1,
    'WPS415': 1,
    'WPS416': 1,
    'WPS417': 1,
    'WPS418': 1,
    'WPS419': 1,
    'WPS420': 2,
    'WPS421': 1,
    'WPS422': 1,
    'WPS423': 1,
    'WPS424': 1,
    'WPS425': 1,
    'WPS426': 1,
    'WPS427': 1,
    'WPS428': 2,
    'WPS429': 1,
    'WPS430': 1,
    'WPS431': 2,
    'WPS432': 2,
    'WPS433': 1,
    'WPS434': 1,
    'WPS435': 1,
    'WPS436': 1,
    'WPS437': 1,
    'WPS438': 4,
    'WPS439': 1,
    'WPS440': 1,
    'WPS441': 1,
    'WPS442': 2,
    'WPS443': 1,
    'WPS444': 1,
    'WPS445': 1,
    'WPS446': 1,
    'WPS447': 1,
    'WPS448': 1,

    'WPS500': 1,
    'WPS501': 1,
    'WPS502': 2,
    'WPS503': 1,
    'WPS504': 1,
    'WPS505': 1,
    'WPS506': 1,
    'WPS507': 1,
    'WPS508': 1,
    'WPS509': 1,
    'WPS510': 1,
    'WPS511': 1,
    'WPS512': 1,
    'WPS513': 1,
    'WPS514': 1,
    'WPS515': 1,
    'WPS516': 1,
    'WPS517': 2,
    'WPS518': 1,
    'WPS519': 1,
    'WPS520': 1,
    'WPS521': 1,

    'WPS600': 1,
    'WPS601': 1,
    'WPS602': 2,
    'WPS603': 1,
    'WPS604': 2,
    'WPS605': 1,
    'WPS606': 1,
    'WPS607': 1,
    'WPS608': 1,
    'WPS609': 1,
    'WPS610': 1,
    'WPS611': 1,
    'WPS612': 1,

    'WPS701': 2,
    'WPS702': 2,
})


def _assert_errors_count_in_output(output, errors, all_violations):
    found_errors = Counter(
        (match.group(0) for match in ERROR_PATTERN.finditer(output)),
    )

    for violation in all_violations:
        key = 'WPS{0}'.format(str(violation.code).zfill(3))
        assert key in errors, 'Unlisted #noqa violation'

    for found_error, found_count in found_errors.items():
        assert found_error in errors, 'Violation without a #noqa count'
        assert found_count == errors.get(found_error)

    assert set(
        filter(lambda key: errors[key] != 0, errors),
    ) - found_errors.keys() == set()


def test_noqa_fixture_disabled(absolute_path, all_violations):
    """End-to-End test to check that all violations are present."""
    process = subprocess.Popen(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--disable-noqa',
            '--isolated',
            '--select',
            'WPS',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    _assert_errors_count_in_output(stdout, SHOULD_BE_RAISED, all_violations)
    assert len(SHOULD_BE_RAISED) == len(all_violations)


def test_noqa_fixture(absolute_path):
    """End-to-End test to check that `noqa` works."""
    process = subprocess.Popen(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--isolated',
            '--select',
            'WPS',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    assert stdout.count('WPS') == 0


def test_noqa_fixture_without_ignore(absolute_path):
    """End-to-End test to check that `noqa` works without ignores."""
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'WPS',
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


def test_noqa_fixture_diff(absolute_path, all_violations):
    """Ensures that our linter works in ``diff`` mode."""
    process = subprocess.Popen(
        [
            'diff',
            '-uN',  # is required to ignore missing files
            'missing_file',  # is required to transform file to diff
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )

    output = subprocess.check_output(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--disable-noqa',
            '--isolated',
            '--diff',  # is required to test diffs! ;)
            '--exit-zero',  # to allow failures
        ],
        stdin=process.stdout,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    process.communicate()

    _assert_errors_count_in_output(output, SHOULD_BE_RAISED, all_violations)
