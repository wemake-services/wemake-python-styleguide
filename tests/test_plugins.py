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
        assert output.count(plugin_code) > 0, plugin_code


def test_external_plugins(absolute_path):
    """End-to-End test to check that all plugins are enabled."""
    filename = absolute_path('fixtures', 'external_plugins.py')
    process = subprocess.Popen(
        [
            'flake8',
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
