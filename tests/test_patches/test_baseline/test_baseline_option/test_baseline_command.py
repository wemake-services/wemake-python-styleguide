"""
We use this test to ensure that ``--baseline`` works correctly.

Here are several important things about this example:

1. There are two violations with the same code and message: ``E225``

2. There are two violations with the same code,
   but different message: ``WPS110``

3. There's a unique violation: ``WPS303``

We also have the second file around with just one ``WPS304`` inside.

All violations in this example are covered by the baseline.
"""

import os
import subprocess

import pytest

from wemake_python_styleguide.logic.baseline import BASELINE_FILE

baseline = """{
  "paths": {
    "other_wrong.py": {
      "e61cb3c3de1cbdac603069903e4af07c": 1
    },
    "wrong.py": {
      "132954ef45e1a84ab72bb6e30126a117": 1,
      "71b49f6407bbc09ac76c372014207dfb": 1,
      "a37c5ca31e3d75d49a018c0bd3ff83f5": 1,
      "dd2402e2213add848d53f8580452417e": 2
    }
  }
}"""

# Templates:

wrong_template = """
value =1
result= 2
undescored_number = 10_0
{0}
"""

wrong_other = 'partial = .5'

# Filenames:

filename_wrong = 'wrong.py'
filename_other = 'other_wrong.py'


def _assert_output(output: str, errors):
    for error_code, error_count in errors.items():
        assert output.count(error_code) == error_count


def test_without_baseline(make_file, read_file):
    """End-to-End test for no baseline yet, initial mode."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)
    cwd = os.path.dirname(filename)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            filename_wrong,
            filename_other,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=cwd,
    )
    output, _ = process.communicate()

    _assert_output(output, {'WPS110': 2, 'WPS303': 1, 'WPS304': 1, 'E225': 2})
    assert process.returncode == 1
    assert read_file(os.path.join(cwd, BASELINE_FILE)) == baseline


@pytest.mark.parametrize('files_to_check', [
    (filename_wrong,),
    (filename_wrong, filename_other),
    (filename_wrong, 'missing.py'),
    (filename_wrong, filename_other, 'missing.py'),
])
def test_with_baseline(make_file, read_file, files_to_check):
    """End-to-End test for baseline generation."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)
    baseline_path = make_file(BASELINE_FILE, baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            *files_to_check,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    assert output == ''
    assert process.returncode == 0
    assert read_file(baseline_path) == baseline


def test_with_baseline_empty(make_file, read_file):
    """End-to-End test that removed violations are fine."""
    filename = make_file(filename_wrong, '_SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            filename_wrong,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    assert output == ''
    assert process.returncode == 0
    assert read_file(baseline_path) == baseline


def test_with_baseline_new_violations(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format('x = 1'))
    baseline_path = make_file(BASELINE_FILE, baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            filename_wrong,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    _assert_output(output, {'WPS111': 1})
    assert process.returncode == 1
    assert read_file(baseline_path) == baseline


def test_with_baseline_new_correct_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file('correct.py', 'SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            filename_wrong,
            'correct.py',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    assert output == ''
    assert process.returncode == 0
    assert read_file(baseline_path) == baseline


def test_with_baseline_new_wrong_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    new_wrong = make_file('new_wrong.py', 'wrong__name = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            filename_wrong,
            'correct.py',
            new_wrong,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    _assert_output(output, {'WPS116': 1})
    assert process.returncode == 1
    assert read_file(baseline_path) == baseline
