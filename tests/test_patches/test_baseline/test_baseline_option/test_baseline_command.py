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

import json
import os
import subprocess
from typing import Dict, Optional

import pytest

from wemake_python_styleguide.logic.baseline import BASELINE_FILE

_FAKE_TIME_METADATA = 'xxxx'

baseline = r"""{
  "metadata": {
    "baseline_file_version": "1",
    "created_at": "xxxx",
    "updated_at": "xxxx"
  },
  "paths": {
    "other_wrong.py": [
      {
        "column": 10,
        "error_code": "WPS304",
        "line": 1,
        "message": "Found partial float: .5",
        "physical_line": "partial = .5"
      }
    ],
    "wrong.py": [
      {
        "column": 0,
        "error_code": "WPS110",
        "line": 2,
        "message": "Found wrong variable name: value",
        "physical_line": "value =1\n"
      },
      {
        "column": 7,
        "error_code": "E225",
        "line": 2,
        "message": "missing whitespace around operator",
        "physical_line": "value =1\n"
      },
      {
        "column": 0,
        "error_code": "WPS110",
        "line": 3,
        "message": "Found wrong variable name: result",
        "physical_line": "result= 2\n"
      },
      {
        "column": 6,
        "error_code": "E225",
        "line": 3,
        "message": "missing whitespace around operator",
        "physical_line": "result= 2\n"
      },
      {
        "column": 20,
        "error_code": "WPS303",
        "line": 4,
        "message": "Found underscored number: 10_0",
        "physical_line": "undescored_number = 10_0\n"
      }
    ]
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

prepend_format = """
{0}
{1}
"""

# Filenames:

filename_wrong = 'wrong.py'
filename_other = 'other_wrong.py'


def _assert_output(
    output: str,
    errors: Dict[str, int],
    lines: Optional[Dict[int, int]] = None,
):
    for error_code, error_count in errors.items():
        assert output.count(error_code) == error_count
    if lines is not None:
        for line, line_count in lines.items():
            assert output.count('.py:{0}:'.format(line)) == line_count


def _safe_baseline(baseline_text: str) -> str:
    baseline_dict = json.loads(baseline_text)
    baseline_dict['metadata']['created_at'] = _FAKE_TIME_METADATA
    baseline_dict['metadata']['updated_at'] = _FAKE_TIME_METADATA
    return json.dumps(baseline_dict, indent=2, sort_keys=True)


def _run_flake8(filename, *flake8_args):
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '.flake8-baseline.json',
            '--select',
            'WPS,E',
            *flake8_args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()
    return output, process.returncode


def test_create_baseline(make_file, read_file):
    """End-to-End test for no baseline yet, initial mode."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)

    output, returncode = _run_flake8(  # noqa: WPS204
        filename, '--create-baseline', filename_wrong, filename_other,
    )

    assert output == ''
    assert returncode == 0
    assert _safe_baseline(
        read_file(os.path.join(os.path.dirname(filename), BASELINE_FILE)),
    ) == baseline


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

    output, returncode = _run_flake8(filename, *files_to_check)

    assert output == ''
    assert returncode == 0
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_baseline_empty(make_file, read_file):
    """End-to-End test that removed violations are fine."""
    filename = make_file(filename_wrong, '_SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    assert output == ''
    assert returncode == 0
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_baseline_new_violations(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format('x = 1'))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS111': 1})
    assert returncode == 1
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_baseline_new_correct_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file('correct.py', 'SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong, 'correct.py')

    assert output == ''
    assert returncode == 0
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_baseline_new_wrong_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    new_wrong = make_file('new_wrong.py', 'undescored_number = 10_0')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong, new_wrong)

    _assert_output(output, {'WPS303': 1})
    assert returncode == 1
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_prepend_errors(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, prepend_format.format(
        'undescored_number = 10_0',
        wrong_template.format(''),
    ))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS303': 1})
    assert returncode == 1
    assert _safe_baseline(read_file(baseline_path)) == baseline


def test_with_prepend_and_postpend_errors(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    new_violation = 'undescored_number = 10_0'
    filename = make_file(filename_wrong, prepend_format.format(
        new_violation,
        wrong_template.format(new_violation),
    ))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS303': 2}, {1: 1, 7: 1})
    assert returncode == 1
    assert _safe_baseline(read_file(baseline_path)) == baseline
