# -*- coding: utf-8 -*-

import subprocess

from wemake_python_styleguide.version import version


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    output = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
    )

    output_text = output.decode('utf-8')
    assert 'wemake-python-styleguide' in output_text
    assert version in output_text
