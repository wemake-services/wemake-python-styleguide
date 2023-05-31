"""
Integration tests definition.

These are integration tests for several things:

1. that violation is active and enabled
2. that violation is raised for the bad code
3. that line number where violation is raised is correct
4. that `noqa` works

See docs:
https://wemake-python-styleguide.rtfd.io/en/latest/pages/api/contributing.html
"""

import re
import subprocess
import sys
import types
from collections import Counter

import pytest

# Versions for different version-specific fixtures.
_PY38 = (3, 8) <= sys.version_info < (3, 9)
_PY39 = (3, 9) <= sys.version_info < (3, 10)
_PY310 = (3, 10) <= sys.version_info < (3, 11)

#: Used to find violations' codes in output.
ERROR_PATTERN = re.compile(r'(WPS\d{3})')

#: List of ignored violations that we do not cover with `noqa` comments.
IGNORED_VIOLATIONS = (
    'WPS201',  # it is a module level violation
    'WPS202',  # since our test case is complex, that's fine
    'WPS203',  # it is a module level violation
    'WPS204',  # our tests have a lot of overused expressions
    'WPS226',  # we have a lot of ugly strings inside

    'WPS400',  # it is a module level violation
    'WPS402',  # we obviously use a lot of `noqa` comments
)

#: Number and count of violations that would be raised.
VERSION_SPECIFIC = types.MappingProxyType({
    'noqa_pre38': {
        'WPS216': 1,
        'WPS224': 1,
        'WPS307': 1,
        'WPS416': 1,
        'WPS602': 2,
    },
    'noqa38': {
        'WPS216': 1,
        'WPS224': 1,
        'WPS307': 1,
        'WPS332': 1,
        'WPS451': 1,
        'WPS452': 1,
        'WPS602': 2,
    },
    'noqa39': {
        'WPS466': 1,
    },
    'noqa310': {
        'WPS110': 1,
        'WPS111': 1,
        'WPS122': 1,
    },
})

#: Number and count of violations that would be raised.
SHOULD_BE_RAISED = types.MappingProxyType({
    'WPS000': 0,  # logically unacceptable.

    'WPS100': 0,  # logically unacceptable.
    'WPS101': 0,  # logically unacceptable.
    'WPS102': 0,  # logically unacceptable.
    'WPS110': 4,
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
    'WPS124': 1,
    'WPS125': 1,

    'WPS200': 0,  # logically unacceptable.
    'WPS201': 0,  # defined in ignored violations.
    'WPS202': 0,  # defined in ignored violations.
    'WPS203': 0,  # defined in ignored violations.
    'WPS204': 0,  # defined in ignored violations.

    'WPS210': 1,
    'WPS211': 1,
    'WPS212': 1,
    'WPS213': 1,
    'WPS214': 1,
    'WPS215': 1,
    'WPS216': 0,  # defined in version specific table.
    'WPS217': 1,
    'WPS218': 1,
    'WPS219': 1,
    'WPS220': 1,
    'WPS221': 2,
    'WPS222': 1,
    'WPS223': 1,
    'WPS224': 0,  # defined in version specific table.
    'WPS225': 1,
    'WPS226': 0,  # defined in ignored violations.
    'WPS227': 2,
    'WPS228': 1,
    'WPS229': 1,
    'WPS230': 1,
    'WPS231': 1,
    'WPS232': 0,  # logically unacceptable.
    'WPS233': 1,
    'WPS234': 1,
    'WPS235': 1,
    'WPS236': 1,
    'WPS237': 1,
    'WPS238': 1,

    'WPS300': 1,
    'WPS301': 1,
    'WPS302': 1,
    'WPS303': 1,
    'WPS304': 1,
    'WPS305': 2,
    'WPS306': 2,
    'WPS307': 0,  # defined in version specific table.
    'WPS308': 1,
    'WPS309': 1,
    'WPS310': 4,
    'WPS311': 1,
    'WPS312': 1,
    'WPS313': 1,
    'WPS314': 1,
    'WPS315': 1,
    'WPS316': 1,
    'WPS317': 1,
    'WPS318': 3,
    'WPS319': 2,
    'WPS320': 2,
    'WPS321': 1,
    'WPS322': 1,
    'WPS323': 1,
    'WPS324': 2,
    'WPS325': 1,
    'WPS326': 1,
    'WPS327': 1,
    'WPS328': 3,
    'WPS329': 1,
    'WPS330': 1,
    'WPS331': 1,
    'WPS332': 0,  # defined in version specific table.
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
    'WPS347': 1,
    'WPS348': 1,
    'WPS349': 1,
    'WPS350': 1,
    'WPS351': 1,
    'WPS352': 1,
    'WPS353': 1,
    'WPS354': 1,
    'WPS355': 1,
    'WPS356': 1,
    'WPS357': 0,  # logically unacceptable.
    'WPS358': 1,
    'WPS359': 1,
    'WPS360': 1,
    'WPS361': 1,
    'WPS362': 2,

    'WPS400': 0,  # defined in ignored violations.
    'WPS401': 0,  # logically unacceptable.
    'WPS402': 0,  # defined in ignored violations.
    'WPS403': 0,  # logically unacceptable.
    'WPS404': 1,
    'WPS405': 1,
    'WPS406': 1,
    'WPS407': 1,
    'WPS408': 1,
    'WPS409': 1,
    'WPS410': 1,
    'WPS411': 0,  # logically unacceptable.
    'WPS412': 0,  # logically unacceptable.
    'WPS413': 1,
    'WPS414': 1,
    'WPS415': 1,
    'WPS416': 0,  # defined in version specific table.
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
    'WPS449': 1,
    'WPS450': 1,
    'WPS451': 0,  # defined in version specific table.
    'WPS452': 1,  # also defined in version specific table.
    'WPS453': 0,
    'WPS454': 1,
    'WPS455': 1,
    'WPS456': 1,
    'WPS457': 1,
    'WPS458': 1,
    'WPS459': 1,
    'WPS460': 1,
    'WPS461': 0,  # logically unacceptable.
    'WPS462': 1,
    'WPS463': 1,
    'WPS464': 0,  # logically unacceptable.
    'WPS465': 1,
    'WPS466': 0,  # defined in version specific table.
    'WPS467': 1,
    'WPS468': 2,
    'WPS469': 1,
    'WPS470': 1,
    'WPS471': 1,
    'WPS472': 1,

    'WPS500': 1,
    'WPS501': 1,
    'WPS502': 2,
    'WPS503': 2,
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
    'WPS522': 1,
    'WPS523': 1,
    'WPS524': 1,
    'WPS525': 2,
    'WPS526': 1,
    'WPS527': 1,
    'WPS528': 1,
    'WPS529': 1,
    'WPS530': 1,
    'WPS531': 1,
    'WPS532': 1,

    'WPS600': 1,
    'WPS601': 1,
    'WPS602': 0,  # defined in version specific table.
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
    'WPS613': 1,
    'WPS614': 1,
    'WPS615': 2,
    'WPS616': 1,
    'WPS473': 0,
})

# Violations which may be tweaked by `i_control_code` option:
SHOULD_BE_RAISED_NO_CONTROL = types.MappingProxyType({
    'WPS113': 0,

    'WPS412': 0,
    'WPS413': 0,
})


def _assert_errors_count_in_output(
    output,
    errors,
    all_violations,
    *,
    total: bool = True,
):
    found_errors = Counter(
        (match.group(0) for match in ERROR_PATTERN.finditer(output)),
    )

    if total:
        for violation in all_violations:
            key = 'WPS{0}'.format(str(violation.code).zfill(3))
            assert key in errors, 'Unlisted #noqa violation'

    for found_error, found_count in found_errors.items():
        assert found_error in errors, 'Violation without a #noqa count'
        assert found_count == errors.get(found_error), found_error

    assert set(
        filter(lambda key: errors[key] != 0, errors),
    ) - found_errors.keys() == set()


def test_codes(all_violations):
    """Ensures that all violations are listed."""
    assert len(SHOULD_BE_RAISED) == len(all_violations)


@pytest.mark.parametrize(('filename', 'violations', 'total'), [
    ('noqa.py', SHOULD_BE_RAISED, True),
    pytest.param(
        'noqa38.py',
        VERSION_SPECIFIC['noqa38'],
        0,
        marks=pytest.mark.skipif(not _PY38, reason='ast changes on 3.8'),
    ),
    pytest.param(
        'noqa39.py',
        VERSION_SPECIFIC['noqa39'],
        0,
        marks=pytest.mark.skipif(not _PY39, reason='ast changes on 3.9'),
    ),
    pytest.param(
        'noqa310.py',
        VERSION_SPECIFIC['noqa310'],
        0,
        marks=pytest.mark.skipif(not _PY310, reason='ast changes on 3.10'),
    ),
])
def test_noqa_fixture_disabled(
    absolute_path,
    all_violations,
    filename,
    violations,
    total,
):
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
            absolute_path('fixtures', 'noqa', filename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    _assert_errors_count_in_output(
        stdout,
        violations,
        all_violations,
        total=total,
    )


def test_noqa_fixture_disabled_no_control(
    absolute_path,
    all_controlled_violations,
):
    """End-to-End test to check rules controlled by `i_control_code` option."""
    process = subprocess.Popen(
        [
            'flake8',
            '--i-dont-control-code',
            '--disable-noqa',
            '--isolated',
            '--select',
            'WPS',
            absolute_path('fixtures', 'noqa', 'noqa_controlled.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    _assert_errors_count_in_output(
        stdout,
        SHOULD_BE_RAISED_NO_CONTROL,
        all_controlled_violations,
    )
    assert len(SHOULD_BE_RAISED_NO_CONTROL) == len(all_controlled_violations)


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
            absolute_path('fixtures', 'noqa', 'noqa.py'),
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
            absolute_path('fixtures', 'noqa', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    for violation in IGNORED_VIOLATIONS:
        assert stdout.count(violation) > 0
