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
  "metadata": [
    "xxxx",
    "xxxx",
    "1"
  ],
  "paths": {
    "other_wrong.py": [
      [
        "WPS304",
        1,
        10,
        "Found partial float: .5",
        "partial = .5"
      ]
    ],
    "wrong.py": [
      [
        "WPS110",
        2,
        0,
        "Found wrong variable name: value",
        "value =1"
      ],
      [
        "E225",
        2,
        7,
        "missing whitespace around operator",
        "value =1"
      ],
      [
        "E225",
        3,
        6,
        "missing whitespace around operator",
        "result= 2"
      ],
      [
        "WPS110",
        3,
        0,
        "Found wrong variable name: result",
        "result= 2"
      ],
      [
        "WPS303",
        4,
        20,
        "Found underscored number: 10_0",
        "undescored_number = 10_0"
      ]
    ]
  }
}"""

baseline_improved = r"""{
  "metadata": [
    "xxxx",
    "xxxx",
    "1"
  ],
  "paths": {
    "other_wrong.py": [
      [
        "WPS304",
        1,
        10,
        "Found partial float: .5",
        "partial = .5"
      ]
    ],
    "wrong.py": [
      [
        "WPS110",
        2,
        0,
        "Found wrong variable name: value",
        "value =1"
      ],
      [
        "WPS110",
        3,
        0,
        "Found wrong variable name: result",
        "result= 2"
      ],
      [
        "WPS303",
        4,
        20,
        "Found underscored number: 10_0",
        "undescored_number = 10_0"
      ]
    ]
  }
}"""

baseline_removed = r"""{
  "metadata": [
    "xxxx",
    "xxxx",
    "1"
  ],
  "paths": {
    "other_wrong.py": [
      [
        "WPS304",
        1,
        10,
        "Found partial float: .5",
        "partial = .5"
      ]
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

wrong_improved = """
value = 1
result = 2
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


def _compare_baseline(  # noqa: WPS210
    baseline_text: str,
    other: Optional[str] = None,
) -> str:
    other_baseline = baseline if other is None else other
    safe_baseline = json.loads(_safe_baseline(baseline_text))
    ref_baseline = json.loads(other_baseline)
    paths1, paths2 = (bl.pop('paths') for bl in (safe_baseline, ref_baseline))
    assert safe_baseline == ref_baseline
    assert paths1.keys() == paths2.keys()

    for filename, violations in paths1.items():
        violations = [tuple(viol) for viol in violations]
        violations2 = [tuple(viol) for viol in paths2[filename]]
        assert len(violations) == len(violations2)
        assert set(violations) == set(violations2)


def _safe_baseline(baseline_text: str) -> str:
    baseline_dict = json.loads(baseline_text)
    baseline_dict['metadata'][0] = _FAKE_TIME_METADATA
    baseline_dict['metadata'][1] = _FAKE_TIME_METADATA
    return json.dumps(baseline_dict, indent=2, sort_keys=True)


def _shift_line_numbers(offset: int) -> str:
    updated_baseline = json.loads(baseline)
    for violation in updated_baseline['paths']['wrong.py']:
        violation[1] += offset
    return json.dumps(updated_baseline)


def _run_flake8(filename, *flake8_args):
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            BASELINE_FILE,
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
    filename = make_file(
        filename_wrong,
        wrong_template.format(''),  # noqa: WPS204
    )
    make_file(filename_other, wrong_other)

    output, returncode = _run_flake8(  # noqa: WPS204
        filename, '--create-baseline',
    )

    msg = 'Created new baseline with 6 violations at:\n./.flake8-baseline.json'
    assert output.strip() == msg
    assert returncode == 0
    _compare_baseline(
        read_file(os.path.join(os.path.dirname(filename), BASELINE_FILE)),
    )


@pytest.mark.parametrize('files_to_check', [
    (filename_wrong,),
    (filename_wrong, filename_other),
])
def test_with_baseline(make_file, read_file, files_to_check):
    """End-to-End test for baseline generation."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)
    baseline_path = make_file(BASELINE_FILE, baseline)  # noqa: WPS204

    output, returncode = _run_flake8(filename, *files_to_check)

    assert output == ''
    assert returncode == 0
    _compare_baseline(read_file(baseline_path))  # noqa: WPS204


def test_with_baseline_empty(make_file, read_file):
    """End-to-End test that removed violations are removed from baseline."""
    filename = make_file(filename_wrong, '_SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    assert output == ''
    assert returncode == 0
    _compare_baseline(read_file(baseline_path), baseline_removed)


def test_with_violation_removed(make_file, read_file):
    """End-to-End test that removed violations are removed from baseline."""
    filename = make_file(filename_wrong, wrong_improved)
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    assert output == ''
    assert returncode == 0
    _compare_baseline(read_file(baseline_path), baseline_improved)


def test_with_violation_changed(make_file, read_file):
    """End-to-End test that changed violations are updated."""
    filename = make_file(filename_wrong, '_SOME_CONSTANT = .5')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    assert output == 'wrong.py:1:18: WPS304 Found partial float: .5\n'
    assert returncode == 0
    _compare_baseline(read_file(baseline_path), baseline_removed)


def test_with_baseline_new_violations(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format('x = 1'))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS111': 1})
    assert returncode == 1
    _compare_baseline(read_file(baseline_path))


def test_with_baseline_new_correct_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file('correct.py', 'SOME_CONSTANT = 1')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong, 'correct.py')

    assert output == ''
    assert returncode == 0
    _compare_baseline(read_file(baseline_path))


def test_with_baseline_new_wrong_files(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)
    new_wrong = make_file('new_wrong.py', 'undescored_number = 10_0')
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong, new_wrong)

    _assert_output(output, {'WPS303': 1})
    assert returncode == 1
    _compare_baseline(read_file(baseline_path))


def test_with_prepend_errors(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    filename = make_file(filename_wrong, prepend_format.format(
        'new_number = 20_0',
        wrong_template.format(''),
    ))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS303': 1})
    assert returncode == 1
    _compare_baseline(read_file(baseline_path), _shift_line_numbers(2))


def test_with_prepend_and_postpend_errors(make_file, read_file):
    """End-to-End test to test that baseline still generates new violations."""
    new_violation = 'new_number = 20_0'
    filename = make_file(filename_wrong, prepend_format.format(
        new_violation,
        wrong_template.format(new_violation),
    ))
    baseline_path = make_file(BASELINE_FILE, baseline)

    output, returncode = _run_flake8(filename, filename_wrong)

    _assert_output(output, {'WPS303': 2}, {2: 1, 7: 1})
    assert returncode == 1
    _compare_baseline(read_file(baseline_path), _shift_line_numbers(2))


def test_with_rename(make_file, read_file):
    """End-to-End test to test that baseline is updated when file is renamed."""
    filename = make_file('renamed_wrong.py', wrong_template.format(''))
    baseline_path = make_file(BASELINE_FILE, baseline)
    renamed_baseline = baseline.replace('"wrong.py"', '"renamed_wrong.py"')

    output, returncode = _run_flake8(filename, 'renamed_wrong.py')

    assert output == ''
    assert returncode == 0
    _compare_baseline(read_file(baseline_path), renamed_baseline)


def test_default_baseline(make_file, read_file):
    """Test that default baseline file is used if no explicit baseline."""
    filename = make_file(filename_wrong, wrong_template.format(''))
    make_file(filename_other, wrong_other)

    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--baseline',
            '--select',
            'WPS,E',
            '--create-baseline',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
        cwd=os.path.dirname(filename),
    )
    output, _ = process.communicate()

    msg = 'Created new baseline with 6 violations at:\n./.flake8-baseline.json'
    assert output.strip() == msg
    assert process.returncode == 0
    _compare_baseline(
        read_file(os.path.join(os.path.dirname(filename), BASELINE_FILE)),
    )


def test_missing_baseline(make_file, read_file):
    """Test that error is emitted if required baseline is missing."""
    filename = make_file(filename_wrong, wrong_template.format(''))

    output, returncode = _run_flake8(filename)

    assert output == (
        'ERROR: No baseline file found ' +
        '(you can create one with --create-baseline).\n'
    )
    assert returncode == 3
