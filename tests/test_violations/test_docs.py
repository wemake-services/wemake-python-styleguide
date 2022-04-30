from wemake_python_styleguide.options.config import Configuration

FORMATTING_OPTIONS = frozenset((
    '--show-violation-links',
))


def test_all_violations_are_documented(all_module_violations):
    """Ensures that all violations are documented."""
    for module, classes in all_module_violations.items():
        for violation_class in classes:
            # Once per `summary` and once per `autoclass`:
            assert module.__doc__.count(violation_class.__qualname__) == 2


def test_all_violations_have_versionadded(all_violations):
    """Ensures that all violations have `versionadded` tag."""
    for violation in all_violations:
        assert '.. versionadded:: ' in violation.__doc__


def test_violation_name(all_violations):
    """Ensures that all violations have `Violation` suffix."""
    for violation in all_violations:
        class_name = violation.__qualname__
        assert class_name.endswith('Violation'), class_name


def test_violation_template_ending(all_violations):
    """Ensures that all violation templates do not end with a dot."""
    for violation in all_violations:
        assert not violation.error_template.endswith('.'), violation


def test_previous_codes_versionchanged(all_violations):
    """Tests that we put both in case violation changes."""
    for violation in all_violations:
        previous_codes = getattr(violation, 'previous_codes', None)
        if previous_codes is not None:
            assert violation.__doc__.count(
                '.. versionchanged::',
            ) >= len(violation.previous_codes)


def test_configuration(all_violations):
    """Ensures that all configuration options are listed in the docs."""
    option_listed = {
        option.long_option_name: False
        for option in Configuration._options  # noqa: WPS437
        if option.long_option_name not in FORMATTING_OPTIONS
    }

    for violation in all_violations:
        for listed in option_listed:
            if listed in violation.__doc__:
                option_listed[listed] = True

                assert 'Configuration:' in violation.__doc__
                assert 'Default:' in violation.__doc__

    for option_item, is_listed in option_listed.items():
        assert is_listed, option_item


def test_all_violations_doc_start_with_full_code(all_violations):
    """Ensures that all violations have `versionadded` tag."""
    for violation in all_violations:
        assert violation.__doc__.lstrip().startswith(violation.full_code)
