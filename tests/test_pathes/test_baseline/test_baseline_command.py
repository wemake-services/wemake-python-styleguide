"""
We use this example together with the existing baseline.

Here are several important things about this example:

1. There are two violations with the same code and message: ``E225``

2. There are two violations with the same code,
   but different message: ``WPS110``

3. There's a unique violation: ``WPS303``

All violations in this example are covered by the baseline.
"""

import os
import subprocess

baseline = """
{
  "paths": {
    "wrong.py": {
      "132954ef45e1a84ab72bb6e30126a117": 1,
      "71b49f6407bbc09ac76c372014207dfb": 1,
      "a37c5ca31e3d75d49a018c0bd3ff83f5": 1,
      "dd2402e2213add848d53f8580452417e": 2
    }
  }
}
"""

code_template = """
value =1
result= 2
undescored_number = 10_0
{0}
"""


def _assert_output(output: str, errors):
    for error_code, error_count in errors.items():
        assert output.count(error_code) == error_count


def test_without_baseline(make_file):
    """End-to-End test for no baseline, regular mode."""
    filename = make_file('wrong.py', code_template.format(''))

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            'wrong.py',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    _assert_output(output, {'WPS110': 2, 'WPS303': 1, 'E225': 2})
    assert process.returncode == 1


def test_with_baseline(make_file):
    """End-to-End test for baseline generation."""
    filename = make_file('wrong.py', code_template.format(''))
    make_file('.flake8-baseline.json', baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            'wrong.py',
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


def test_with_baseline_empty(make_file):
    """End-to-End test that removed violations are fine."""
    filename = make_file('wrong.py', '_SOME_CONSTANT = 1')
    make_file('.flake8-baseline.json', baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            'wrong.py',
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


def test_with_baseline_new_violations(make_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file('wrong.py', code_template.format('x = 1'))
    make_file('.flake8-baseline.json', baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            'wrong.py',
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


def test_with_baseline_new_files(make_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file('wrong.py', code_template.format(''))
    make_file('correct.py', 'SOME_CONSTANT = 1')
    make_file('.flake8-baseline.json', baseline)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            'wrong.py',
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
