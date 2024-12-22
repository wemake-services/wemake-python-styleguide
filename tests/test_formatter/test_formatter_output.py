"""
We use direct string assertiong on the formatter.

So, no unit tests for formatter, only e2e ones.

We use ``surupy`` to render and assert equality of the output:
https://github.com/tophat/syrupy

To update snapshots use ``--snapshot-update`` flag, when running ``pytest``.

We also don't use ``absolute_path`` fixture here,
because it renders differently on different envs.

Warning::

    Files inside ``./__snapshots__`` are auto generated!
    Do not edit them manually.

"""

import os
import subprocess
from pathlib import Path

import pytest

from wemake_python_styleguide.formatter import WemakeFormatter
from wemake_python_styleguide.version import pkg_version


def _safe_output(output: str) -> str:
    """
    Removes version specific things from console output.

    So our formatter will be tested on all versions correctly.
    """
    assert pkg_version, 'Looks like version is broken'

    current_version_url = WemakeFormatter._doc_url  # noqa: WPS437
    general_version_url = current_version_url.replace(pkg_version, 'xx.xx')
    return output.replace(current_version_url, general_version_url)


@pytest.mark.parametrize(
    ('cli_options', 'output'),
    [
        ([], 'regular'),
        (['--statistic'], 'regular_statistic'),
        (['--show-source'], 'with_source'),
        (['--show-violation-links'], 'with_links'),
        (['--show-source', '--statistic'], 'with_source_statistic'),
        (['--show-source', '--show-violation-links'], 'with_source_links'),
        (['--statistic', '--show-source'], 'statistic_with_source'),
    ],
)
@pytest.mark.parametrize(
    'no_color',
    [True, False, None],
    ids=['without_colors', 'with_colors', 'default_colors'],
)
def test_formatter(snapshot, cli_options, output, no_color):
    """
    End-to-End test to that formatting works well.

    We only use ``WPS`` because other violations order is unpredictable.
    Since ``flake8`` plugins work in parallel.
    """
    filename1 = './tests/fixtures/formatter/formatter1.py'
    filename2 = './tests/fixtures/formatter/formatter2.py'
    if no_color is None:
        env = os.environ
    else:
        env = {**os.environ, 'NO_COLOR': '1' if no_color else '0'}

    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--select',
            'WPS',
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
        env=env,
    )
    stdout, _ = process.communicate()

    assert _safe_output(stdout) == snapshot, f'formatter_{output}_{no_color}'


@pytest.mark.parametrize(
    ('cli_options', 'output'),
    [
        ([], 'regular'),
        (['--statistic'], 'regular_statistic'),
        (['--show-source'], 'with_source'),
        (['--show-violation-links'], 'with_links'),
        (['--show-source', '--statistic'], 'with_source_statistic'),
        (['--show-source', '--show-violation-links'], 'with_source_links'),
        (['--statistic', '--show-source'], 'statistic_with_source'),
    ],
)
@pytest.mark.parametrize(
    'no_color',
    [True, False],
    ids=['without_colors', 'with_colors'],
)
def test_formatter_correct(snapshot, cli_options, output, no_color):
    """All correct code should not raise any violations and no output."""
    filename = './tests/fixtures/formatter/correct.py'

    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            '--select',
            'WPS',
            '--format',
            'wemake',
            *cli_options,
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        env={**os.environ, 'NO_COLOR': '1' if no_color else '0'},
    )
    stdout, stderr = process.communicate()
    assert process.returncode == 0, (stdout, stderr)

    assert _safe_output(stdout) == snapshot, (
        f'formatter_correct_{output}_{no_color}'
    )


def test_ipynb(snapshot):
    """All correct code should not raise any violations and no output."""
    filename = './tests/fixtures/notebook.ipynb'
    # Ignore error codes which don't apply to Jupyter Notebooks
    cli_options = [
        '--extend-ignore',
        'WPS102,WPS114,WPS116,WPS124',
    ]

    process = subprocess.Popen(
        [
            'nbqa',
            'flake8',
            filename,
            '--disable-noqa',
            '--isolated',
            '--format',
            'wemake',
            *cli_options,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    stdout, _ = process.communicate()

    # nbQA output contains absolute path
    stdout = stdout.replace(f'{Path.cwd()}{os.sep}', '')

    assert _safe_output(stdout) == snapshot, 'formatter_ipynb'
