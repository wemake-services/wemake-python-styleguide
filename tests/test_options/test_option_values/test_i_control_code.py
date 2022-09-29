"""
This is a regression test for the argument parsing issue for boolean args.

.. versionadded:: 0.13.0

See also:
    - https://github.com/wemake-services/wemake-python-styleguide/issues/966
    - https://stackoverflow.com/a/15008806/4842742

"""


def test_parsing_i_control_code(option_parser):
    """Ensures that ``i_control_code`` can be parsed."""
    namespace = option_parser.parse_args(['--i-control-code'])
    try:
        args, _ = namespace  # flake8 < 5
    except TypeError:
        args = namespace
    assert args.i_control_code is True


def test_parsing_i_dont_control_code(option_parser):
    """Ensures that ``i_dont_control_code`` can be parsed."""
    namespace = option_parser.parse_args(['--i-dont-control-code'])
    try:
        args, _ = namespace  # flake8 < 5
    except TypeError:
        args = namespace
    assert args.i_control_code is False
