"""
These test ensures that each plugin is enabled and working.

We only test a single warning from each plugin.
We do not test that any of the 3rd party plugins work correctly.

It is not our responsibility.
"""


import subprocess

PLUGINS = (
    'B002',  # flake8-bugbear
    'C400',  # flake8-comprehensions
    'C819',  # flake8-commas
    'D103',  # flake8-docstring
    'E225',  # pycodestyle
    'E800',  # flake8-eradicate
    'F401',  # pyflakes
    'I001',  # flake8-isort
    'N400',  # flake8-broken-line
    'N802',  # pep8-naming
    'P101',  # flake8-string-format
    'Q003',  # flake8-quotes
    'S101',  # flake8-bandit
    'T100',  # flake8-debugger
    'RST215',  # flake8-rst-docstrings
    'DAR101',  # darglint
)


def _assert_plugin_output(output):
    for plugin_code in PLUGINS:
        assert output.count(plugin_code) > 0


def test_external_plugins(absolute_path):
    """End-to-End test to check that all plugins are enabled."""
    filename = absolute_path('fixtures', 'external_plugins.py')
    process = subprocess.Popen(
        [
            'flake8',
            '--disable-noqa',
            '--isolated',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    output, _ = process.communicate()

    _assert_plugin_output(output)


def test_external_plugins_diff(absolute_path):
    """Ensures that our linter and all plugins work in ``diff`` mode."""
    process = subprocess.Popen(
        [
            'diff',
            '-uN',  # is required to ignore missing files
            'missing_file',  # is required to transform file to diff
            absolute_path('fixtures', 'external_plugins.py'),
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
    process.communicate()

    _assert_plugin_output(output)
