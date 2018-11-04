# -*- coding: utf-8 -*-

from contextlib import suppress

import pytest

from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.violations.naming import (
    ReservedArgumentNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming import WrongNameVisitor


@pytest.mark.parametrize('argument', SPECIAL_ARGUMENT_NAMES_WHITELIST)
def test_restricted_argument_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    naming_template,
    default_options,
    mode,
    argument,
):
    """Ensures that special names for arguments are restricted."""
    with suppress(SyntaxError):
        tree = parse_ast_tree(mode(naming_template.format(argument)))

        visitor = WrongNameVisitor(default_options, tree=tree)
        visitor.run()

        assert_errors(visitor, [ReservedArgumentNameViolation])
        assert_error_text(visitor, argument)
