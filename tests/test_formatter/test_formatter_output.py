# -*- coding: utf-8 -*-

"""
We use direct string assertiong on the formatter.

So, no unit tests for formatter, only e2e ones.

We use ``snapshottest`` to render and assert equality of the output:
https://github.com/syrusakbary/snapshottest

To update snapshots use ``--snapshot-update`` flag, when running ``pytest``.

Warning::

    Files inside ``./snapshots`` are auto generated!
    Do not edit them manually.

"""


import subprocess

import pytest


@pytest.mark.parametrize('cli_options, output', [
    ([], 'regular'),
    (['--statistic'], 'regular_statistic'),
    (['--show-source'], 'with_source'),
    (['--show-source', '--statistic'], 'with_source_statistic'),
    (['--statistic', '--show-source'], 'statistic_with_source'),
])
def test_formatter(snapshot, cli_options, output):
    """
    End-to-End test to that formatting works well.

    We only use ``Z`` because other violations order is unpredictable.
    Since ``flake8`` plugins work in parallel.
    """
    filename1 = './tests/fixtures/formatter1.py'
    filename2 = './tests/fixtures/formatter2.py'

    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--select',
            'Z',
            '--format',
            'wemake',
            *cli_options,
            filename1,
            filename2,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    snapshot.assert_match(stdout, 'formatter_{0}'.format(output))


@pytest.mark.parametrize('cli_options, output', [
    ([], 'regular'),
    (['--statistic'], 'regular_statistic'),
    (['--show-source'], 'with_source'),
    (['--show-source', '--statistic'], 'with_source_statistic'),
    (['--statistic', '--show-source'], 'statistic_with_source'),
])
def test_formatter_correct(snapshot, cli_options, output):
    """All correct code should not raise any violations and no output."""
    filename = './tests/fixtures/correct.py'

    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--format',
            'wemake',
            *cli_options,
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    snapshot.assert_match(stdout, 'formatter_correct_{0}'.format(output))
