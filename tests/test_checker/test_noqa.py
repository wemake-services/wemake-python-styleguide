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
import types
from collections import Counter
from typing import Final

import pytest

from wemake_python_styleguide.compat.constants import PY313

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

#: List of ignored violations on python 3.13+.
IGNORED_VIOLATIONS3_13 = ()

#: Number and count of violations that would be raised.
SHOULD_BE_RAISED = types.MappingProxyType(
    {
        'WPS000': 0,  # logically unacceptable.
        'WPS100': 0,  # logically unacceptable.
        'WPS101': 0,  # logically unacceptable.
        'WPS102': 0,  # logically unacceptable.
        'WPS110': 5,
        'WPS111': 2,
        'WPS112': 1,
        'WPS113': 0,  # disabled since 1.0.0
        'WPS114': 1,
        'WPS115': 1,
        'WPS116': 1,
        'WPS117': 1,
        'WPS118': 1,
        'WPS119': 0,  # disabled since 1.0.0
        'WPS120': 1,
        'WPS121': 1,
        'WPS122': 2,
        'WPS123': 1,
        'WPS124': 1,
        'WPS125': 0,  # disabled since 1.0.0
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
        'WPS216': 1,
        'WPS217': 1,
        'WPS218': 1,
        'WPS219': 1,
        'WPS220': 1,
        'WPS221': 2,
        'WPS222': 1,
        'WPS223': 1,
        'WPS224': 1,
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
        'WPS239': 1,
        'WPS240': 0,  # only triggers on 3.12+
        'WPS241': 1,
        'WPS242': 1,
        'WPS243': 1,
        'WPS300': 1,
        'WPS301': 1,
        'WPS302': 0,  # disabled since 1.0.0
        'WPS303': 1,
        'WPS304': 0,  # disabled since 1.0.0
        'WPS305': 0,
        'WPS306': 0,  # disabled since 1.0.0
        'WPS307': 1,
        'WPS308': 1,
        'WPS309': 0,  # disabled since 1.0.0
        'WPS310': 0,  # disabled since 1.0.0
        'WPS311': 1,
        'WPS312': 0,  # disabled since 1.0.1
        'WPS313': 0,  # disabled since 1.0.0
        'WPS314': 1,
        'WPS315': 0,  # disabled since 1.0.0
        'WPS316': 0,  # disabled since 1.0.0
        'WPS317': 0,  # disabled since 1.0.0
        'WPS318': 0,  # disabled since 1.0.0
        'WPS319': 0,  # disabled since 1.0.0
        'WPS320': 0,  # disabled since 1.0.0
        'WPS321': 1,
        'WPS322': 1,
        'WPS323': 0,  # disabled since 1.0.0
        'WPS324': 2,
        'WPS325': 1,
        'WPS326': 0,  # disabled since 1.0.0
        'WPS327': 1,
        'WPS328': 3,
        'WPS329': 0,  # disabled since 1.0.0
        'WPS330': 1,
        'WPS331': 0,  # disabled since 1.0.0
        'WPS332': 1,
        'WPS333': 0,  # disabled since 1.0.0
        'WPS334': 1,
        'WPS335': 1,
        'WPS336': 1,
        'WPS337': 0,  # disabled since 1.0.0
        'WPS338': 1,
        'WPS339': 1,
        'WPS340': 0,  # disabled since 1.0.0
        'WPS341': 0,  # disabled since 1.0.0
        'WPS342': 1,
        'WPS343': 0,  # disabled since 1.0.0
        'WPS344': 1,
        'WPS345': 1,
        'WPS346': 1,
        'WPS347': 1,
        'WPS348': 0,  # disabled since 1.0.0
        'WPS349': 1,
        'WPS350': 1,
        'WPS351': 0,  # disabled since 1.0.0
        'WPS352': 0,  # disabled since 1.0.0
        'WPS353': 1,
        'WPS354': 0,  # disabled since 1.6.0
        'WPS355': 0,  # disabled since 1.0.0
        'WPS356': 1,
        'WPS357': 0,  # logically unacceptable.
        'WPS358': 1,
        'WPS359': 1,
        'WPS360': 0,  # disabled since 1.0.0
        'WPS361': 0,  # disabled since 1.0.0
        'WPS362': 2,
        'WPS363': 1,
        'WPS364': 1,
        'WPS365': 1,
        'WPS366': 1,
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
        'WPS415': 0,  # disabled since 1.0.0
        'WPS416': 0,  # deprecated
        'WPS417': 0,  # disabled since 1.0.0
        'WPS418': 1,
        'WPS419': 0,  # disabled since 1.0.0
        'WPS420': 2,
        'WPS421': 1,
        'WPS422': 1,
        'WPS423': 0,  # disabled since 1.0.0
        'WPS424': 0,  # disabled since 1.0.0
        'WPS425': 0,  # disabled since 1.0.0
        'WPS426': 1,
        'WPS427': 1,
        'WPS428': 0,  # disabled since 1.0.0
        'WPS429': 1,
        'WPS430': 3,
        'WPS431': 2,
        'WPS432': 2,
        'WPS433': 0,  # disabled since 1.0.0
        'WPS434': 0,  # disabled since 1.0.0
        'WPS435': 1,
        'WPS436': 0,  # disabled since 1.0.0
        'WPS437': 0,  # disabled since 1.0.0
        'WPS438': 4,
        'WPS439': 1,
        'WPS440': 0,  # disabled since 1.0.0
        'WPS441': 1,
        'WPS442': 0,  # disabled since 1.0.0
        'WPS443': 1,
        'WPS444': 1,
        'WPS445': 1,
        'WPS446': 1,
        'WPS447': 1,
        'WPS448': 1,
        'WPS449': 1,
        'WPS450': 0,  # disabled since 1.0.0
        'WPS451': 0,  # deprecated
        'WPS452': 0,  # disabled since 1.0.0
        'WPS453': 0,
        'WPS454': 0,  # disabled since 1.0.0
        'WPS455': 1,
        'WPS456': 0,  # disabled since 1.0.0
        'WPS457': 1,
        'WPS458': 1,
        'WPS459': 1,
        'WPS460': 1,
        'WPS461': 0,  # logically unacceptable.
        'WPS462': 1,
        'WPS463': 1,
        'WPS464': 0,  # logically unacceptable.
        'WPS465': 0,  # disabled since 1.0.0
        'WPS466': 1,
        'WPS467': 0,  # disabled since 1.0.0
        'WPS468': 2,
        'WPS469': 1,
        'WPS470': 1,
        'WPS471': 1,
        'WPS472': 1,
        'WPS473': 0,
        'WPS474': 1,
        'WPS475': 1,
        'WPS476': 1,
        'WPS477': 0,  # enabled only in python 3.13+
        'WPS478': 1,
        'WPS479': 0,
        'WPS480': 0,  # only triggers on 3.12+
        'WPS481': 10,
        'WPS500': 1,
        'WPS501': 1,
        'WPS502': 0,  # disabled since 1.0.0
        'WPS503': 0,  # disabled since 1.0.0
        'WPS504': 1,
        'WPS505': 1,
        'WPS506': 1,
        'WPS507': 0,  # disabled since 1.0.0
        'WPS508': 0,  # disabled since 1.0.0
        'WPS509': 1,
        'WPS510': 0,  # disabled since 1.0.0
        'WPS511': 0,  # disabled since 1.0.0
        'WPS512': 0,  # disabled since 1.0.0
        'WPS513': 1,
        'WPS514': 0,  # disabled since 1.0.0
        'WPS515': 1,
        'WPS516': 1,
        'WPS517': 2,
        'WPS518': 1,
        'WPS519': 1,
        'WPS520': 1,
        'WPS521': 0,  # disabled since 1.0.0
        'WPS522': 1,
        'WPS523': 1,
        'WPS524': 1,
        'WPS525': 0,  # disabled since 1.0.0
        'WPS526': 0,  # disabled since 1.0.0
        'WPS527': 1,
        'WPS528': 0,  # disabled since 1.0.0
        'WPS529': 1,
        'WPS530': 1,
        'WPS531': 0,  # disabled since 1.0.0
        'WPS532': 1,
        'WPS533': 1,
        'WPS534': 1,
        'WPS535': 1,
        'WPS536': 1,
        'WPS600': 1,
        'WPS601': 1,
        'WPS602': 2,
        'WPS603': 1,
        'WPS604': 1,
        'WPS605': 1,
        'WPS606': 1,
        'WPS607': 1,
        'WPS608': 1,
        'WPS609': 0,  # disabled since 1.0.0
        'WPS610': 1,
        'WPS611': 1,
        'WPS612': 1,
        'WPS613': 1,
        'WPS614': 1,
        'WPS615': 2,
        'WPS616': 1,
        'WPS617': 1,
    },
)

#: Number and count of violations that would be raised.
SHOULD_BE_RAISED3_13 = types.MappingProxyType({'WPS477': 1})


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

    if total:  # pragma: no cover
        for violation in all_violations:
            key = f'WPS{str(violation.code).zfill(3)}'  # noqa: WPS237
            assert key in errors, 'Unlisted #noqa violation'

    for found_error, found_count in found_errors.items():
        assert found_error in errors, 'Violation without a #noqa count'
        assert found_count == errors.get(found_error), found_error

    assert set(found_errors.keys()) == set(
        filter(lambda key: errors[key] != 0, errors),  # expected
    )


def test_codes(all_violations):
    """Ensures that all violations are listed."""
    assert len(SHOULD_BE_RAISED) == len(all_violations)


ALWAYS: Final = True  # just for beautiful condition def


@pytest.mark.parametrize(
    ('filename', 'violations', 'run_condition'),
    [
        ('noqa.py', SHOULD_BE_RAISED, ALWAYS),
        ('noqa313.py', SHOULD_BE_RAISED3_13, PY313),
    ],
)
def test_noqa_fixture_disabled(
    absolute_path,
    all_violations,
    filename,
    violations,
    run_condition,
):
    """End-to-End test to check that all violations are present."""
    if not run_condition:  # pragma: no cover
        return
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
    stdout, stderr = process.communicate()

    assert stdout
    assert not stderr.count('WPS')
    _assert_errors_count_in_output(
        stdout,
        violations,
        all_violations,
        total=filename == 'noqa.py',
    )


@pytest.mark.parametrize(
    ('filename', 'run_condition'),
    [
        ('noqa.py', ALWAYS),
        ('noqa313.py', PY313),
    ],
)
def test_noqa_fixture(absolute_path, filename, run_condition):
    """End-to-End test to check that `noqa` works."""
    if not run_condition:  # pragma: no cover
        return
    process = subprocess.Popen(
        [
            'flake8',
            '--ignore',
            ','.join(IGNORED_VIOLATIONS),
            '--isolated',
            '--select',
            'WPS, E999',
            absolute_path('fixtures', 'noqa', filename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, stderr = process.communicate()

    assert not stdout
    assert not stderr.count('WPS')


@pytest.mark.parametrize(
    ('filename', 'ignored_violations', 'run_condition'),
    [
        ('noqa.py', IGNORED_VIOLATIONS, ALWAYS),
        ('noqa313.py', IGNORED_VIOLATIONS3_13, PY313),
    ],
)
def test_noqa_fixture_without_ignore(
    absolute_path,
    filename,
    ignored_violations,
    run_condition,
):
    """End-to-End test to check that `noqa` works without ignores."""
    if not run_condition:  # pragma: no cover
        return
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'WPS, E999',
            absolute_path('fixtures', 'noqa', filename),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    for violation in ignored_violations:
        assert stdout.count(violation) > 0
