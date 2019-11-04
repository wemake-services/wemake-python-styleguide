# -*- coding: utf-8 -*-

import ast
from contextlib import suppress

from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.violations.system import InternalErrorViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class _BrokenVisitor(BaseNodeVisitor):
    def visit(self, _tree) -> None:
        raise ValueError('Message from visitor')


def test_exception_handling(
    default_options,
    capsys,
):
    """Ensures that checker works with module names."""
    Checker.parse_options(default_options)
    checker = Checker(tree=ast.parse(''), file_tokens=[], filename='test.py')
    checker._visitors = [_BrokenVisitor]  # noqa: WPS437

    with suppress(StopIteration):
        violation = next(checker.run())
        assert violation[2][7:] == InternalErrorViolation.error_template

    captured = capsys.readouterr()
    assert 'ValueError: Message from visitor' in captured.out
