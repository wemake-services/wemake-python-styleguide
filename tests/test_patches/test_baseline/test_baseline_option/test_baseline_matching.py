"""
Test fuzzy matching algorithm.

We use this test to ensure to ensure typical code changes are correctly
matched by the fuzzy matching algorithm and don't emit previously ignored
errors.
"""

import os
import subprocess

import pytest

from wemake_python_styleguide.logic.baseline import BASELINE_FILE

TEST_FILENAME = 'test_file.py'

move_line_init = """
result= 2
"""
move_line_change = """
# New line
result= 2
"""
move_line = (move_line_init, move_line_change)

move_col_init = """
cond_val = True

result= 2
"""
move_col_change = """
cond_val = True
if cond_val:
    result= 2
"""
move_col = (move_col_init, move_col_change)

rename_init = """
result= 2
"""
rename_change = """
new_name= 2
"""
rename = (rename_init, rename_change)

# Line and col changed.
block_init = """
result= 2
"""
block_change = """
cond_val = True
if cond_val:
    result= 2
"""
block = (block_init, block_change)

# Same error/col on adjacent lines. Line shifts so errors overlap.
multierror_line_init = """
one_error= 2
same_here= 3
"""
multierror_line_change = """
# Errors shifted one line.
one_error= 2
same_here= 3
"""
multierror_line = (multierror_line_init, multierror_line_change)

# line, col, physical_line all changed.
all_change_init = """
def some_method(first_arg, second_arg =5):
    return True
"""
all_change_change = """
cond_val = True
if cond_val:
    def renamed_method(first_arg, num_arg =5):
        return True
"""
all_change = (all_change_init, all_change_change)

# Simulate a series of multiple changes.
# The end result looks nothing like the starting point, but we should
# still be able to catch this by updating the baseline with each change.
multi_change_init = """
def some_method(first_arg, second_arg =5):
    return True
"""
multi_change_change1 = """
cond_val = True


def some_method(first_arg, second_arg =5):
    return True
"""
multi_change_change2 = """
cond_val = True


def renamed(simple_arg, num_arg =5, **kwargs):
    return True
"""
multi_change_change3 = """
cond_val = True

if cond_val:
    def renamed(simple_arg, num_arg =5, **kwargs):
        return True
"""
multi_change_change4 = """
cond_val = True

if cond_val:
    def renamed(simple, num =5, **kwargs):
        return False
"""
multi_change = (
    multi_change_init,
    multi_change_change1,
    multi_change_change2,
    multi_change_change3,
    multi_change_change4,
)


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


# TODO: Add rename, all_change. Looser fuzzy matching can match this in future.
@pytest.mark.parametrize('file_states', [  # noqa: WPS210
    move_line,
    move_col,
    block,
    multierror_line,
    multi_change,
])
def test_baseline_matching(make_file, read_file, file_states):  # noqa: WPS210
    """Test that fuzzy matchers catch these sequence of changes."""
    file_initial, *file_changes = file_states
    filename = make_file(TEST_FILENAME, file_initial)

    output, returncode = _run_flake8(filename, '--create-baseline')

    assert 'Created new baseline' in output
    assert returncode == 0

    for updated_file in file_changes:
        with open(filename, 'w') as file_obj:
            file_obj.write(updated_file)

        output, returncode = _run_flake8(filename)

        assert output == ''
        assert returncode == 0
