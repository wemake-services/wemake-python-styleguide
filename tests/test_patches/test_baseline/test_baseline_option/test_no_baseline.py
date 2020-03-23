import os
import subprocess

import pytest

from wemake_python_styleguide.logic.baseline import BASELINE_FILE


def test_no_baseline_option(make_file, read_file):
    """End-to-End test for no baseline, regular mode."""
    filename = make_file('wrong.py', 'x = 1')
    cwd = os.path.dirname(filename)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'WPS,E',
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=cwd,
    )
    output, _ = process.communicate()

    assert process.returncode == 1
    with pytest.raises(IOError, match=BASELINE_FILE):
        read_file(os.path.join(cwd, BASELINE_FILE))
