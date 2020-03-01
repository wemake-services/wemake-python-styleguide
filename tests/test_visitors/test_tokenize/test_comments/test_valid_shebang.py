# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import ShebangViolation
from wemake_python_styleguide.visitors.tokenize.comments import ShebangVisitor

# Correct

exe001_neg_shouldnt_be_executable = """
if __name__ == '__main__':
    print('I am not executable.')
"""

exe001_neg_executable = False
exe001_neg_filename = 'exe001_neg.py'

exe002_neg_shouldnt_be_executable = """
def a_lib_function():
    print('I am not executable.')
"""

exe002_neg_executable = False
exe002_neg_filename = 'exe002_neg.py'

exe003_neg_good_shebang = """#!/usr/bin/python3

if __name__ == '__main__':
    print('I have a good shebang.')
"""

exe003_neg_executable = True
exe003_neg_filename = 'exe003_neg.py'

exe004_neg_no_space_before_shebang = """#!/usr/bin/python3

if __name__ == '__main__':
    print('I do not have whitespace before shebang.')
"""

exe004_neg_executable = True
exe004_neg_filename = 'exe004_neg.py'

exe005_neg_nothing_before_shebang = """#!/usr/bin/python3

if __name__ == '__main__':
    print('I do not have any blank or comment lines before shebang.')
"""

exe005_neg_executable = True
exe005_neg_filename = 'exe005_neg.py'

# Wrong

exe001_pos_should_be_executable = """#!/usr/bin/python

if __name__ == '__main__':
    print('I should be executable.')
"""

exe001_pos_executable = False
exe001_pos_filename = 'exe001_pos.py'

exe002_pos_shouldnt_be_executable = """
def a_lib_function():
    print("I shouldn't be executable.")
"""

exe002_pos_executable = True
exe002_pos_filename = 'exe002_pos.py'

exe003_pos_good_shebang = """#!/bin/bash

if __name__ == '__main__':
    print('I have a wrong shebang.')
"""

exe003_pos_executable = True
exe003_pos_filename = 'exe003_pos.py'

exe004_pos_no_space_before_shebang = """    #!/usr/bin/python3

if __name__ == '__main__':
    print('I have whitespace before shebang.')
"""

exe004_pos_executable = True
exe004_pos_filename = 'exe004_pos.py'

exe005_pos_nothing_before_shebang = """
#
#!/usr/bin/python3

if __name__ == '__main__':
    print('I have blank and comment lines before shebang.')
"""

exe005_pos_executable = True
exe005_pos_filename = 'exe005_pos.py'


@pytest.mark.parametrize(('filename', 'file_content', 'executable'), [
    (
        exe001_neg_filename,
        exe001_neg_shouldnt_be_executable,
        exe001_neg_executable,
    ),
    (
        exe002_neg_filename,
        exe002_neg_shouldnt_be_executable,
        exe002_neg_executable,
    ),
    (
        exe003_neg_filename,
        exe003_neg_good_shebang,
        exe003_neg_executable,
    ),
    (
        exe004_neg_filename,
        exe004_neg_no_space_before_shebang,
        exe004_neg_executable,
    ),
    (
        exe005_neg_filename,
        exe005_neg_nothing_before_shebang,
        exe005_neg_executable,
    ),
])
def test_exe_negative(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    filename,
    file_content,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(filename, file_content, executable)
    file_tokens = parse_file_tokens(path_to_file)

    visitor = ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize(('filename', 'file_content', 'executable'), [
    (
        exe001_pos_filename,
        exe001_pos_should_be_executable,
        exe001_pos_executable,
    ),
    (
        exe002_pos_filename,
        exe002_pos_shouldnt_be_executable,
        exe002_pos_executable,
    ),
    (
        exe003_pos_filename,
        exe003_pos_good_shebang,
        exe003_pos_executable,
    ),
    (
        exe004_pos_filename,
        exe004_pos_no_space_before_shebang,
        exe004_pos_executable,
    ),
    (
        exe005_pos_filename,
        exe005_pos_nothing_before_shebang,
        exe005_pos_executable,
    ),
])
def test_exe_posititve(
    make_file,
    assert_errors,
    parse_file_tokens,
    default_options,
    filename,
    file_content,
    executable,
):
    """Testing cases when no errors should be reported."""
    path_to_file = make_file(filename, file_content, executable)
    file_tokens = parse_file_tokens(path_to_file)

    visitor = ShebangVisitor(
        default_options,
        filename=path_to_file,
        file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [ShebangViolation])
