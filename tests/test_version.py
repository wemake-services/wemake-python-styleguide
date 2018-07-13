# -*- coding: utf-8 -*-

import subprocess


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    output = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
    )
    assert b'wemake-python-styleguide' in output
