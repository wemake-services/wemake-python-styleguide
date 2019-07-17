# -*- coding: utf-8 -*-

import re
import subprocess
import types
from collections import Counter

ERROR_PATTERN = re.compile(r'(WPS\d{3})')
IGNORED_VIOLATIONS = (
    'WPS202',  # since our test case is complex, that's fine
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

    'WPS200': 0,
    'WPS201': 0,
    'WPS202': 0,

    'WPS210': 1,
    'WPS211': 1,
    'WPS212': 1,
    'WPS213': 1,
    'WPS214': 0,
    'WPS215': 1,
    'WPS216': 0,
    'WPS217': 1,

    'WPS220': 1,
    'WPS221': 2,
    'WPS222': 1,
    'WPS223': 1,
    'WPS224': 1,
    'WPS225': 1,
    'WPS226': 0,
    'WPS227': 1,
    'WPS228': 1,

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

    'WPS400': 0,
    'WPS401': 0,
    'WPS402': 0,
    'WPS403': 0,

    'WPS410': 1,
    'WPS411': 0,
    'WPS412': 0,
    'WPS413': 1,

    'WPS420': 2,
    'WPS421': 1,
    'WPS422': 1,
    'WPS423': 1,
    'WPS424': 1,
    'WPS425': 1,
    'WPS426': 1,
    'WPS427': 1,

    'WPS430': 1,
    'WPS431': 2,
    'WPS432': 2,
    'WPS433': 2,
    'WPS434': 1,
    'WPS435': 1,
    'WPS436': 1,
    'WPS437': 1,
    'WPS438': 1,
    'WPS439': 1,
    'WPS440': 1,
    'WPS441': 1,
    'WPS442': 1,
    'WPS443': 1,
    'WPS444': 2,
    'WPS445': 1,
    'WPS446': 1,
    'WPS447': 1,
    'WPS448': 1,
    'WPS449': 1,
    'WPS450': 1,
    'WPS451': 2,
    'WPS452': 2,
    'WPS453': 1,
    'WPS454': 1,
    'WPS455': 1,
    'WPS456': 1,
    'WPS457': 1,
    'WPS458': 1,
    'WPS459': 1,
    'WPS460': 1,
    'WPS461': 1,
    'WPS462': 1,
    'WPS463': 1,
    'WPS464': 1,
    'WPS465': 1,
    'WPS466': 1,
    'WPS467': 1,
    'WPS468': 1,
    'WPS469': 1,
    'WPS470': 1,
    'WPS471': 1,
    'WPS472': 1,
    'WPS473': 1,
    'WPS474': 1,
    'WPS475': 1,
})


def _assert_errors_count_in_output(output, errors, all_violations):
    found_errors = Counter((
        match.group(0) for match in ERROR_PATTERN.finditer(output)
    ))

    for violation in all_violations:
        key = 'WPS' + str(violation.code).zfill(3)
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
    process.wait()

    _assert_errors_count_in_output(output, SHOULD_BE_RAISED, all_violations)
