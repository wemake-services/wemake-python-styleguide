# -*- coding: utf-8 -*-


def test_all_violations_are_documented(all_module_violations):
    """Ensures that all violations are documented."""
    for module, classes in all_module_violations.items():
        for violation_class in classes:
            # Once per `summary` and once per `autoclass`:
            assert module.__doc__.count(violation_class.__qualname__) == 2


def test_all_violations_have_description_with_code(all_violations):
    """Ensures that all violations have description with violation code."""
    for violation in all_violations:
        assert str(violation.code) in violation.__doc__


def test_all_violations_have_versionadded(all_violations):
    """Ensures that all violations have `versionadded` tag."""
    for violation in all_violations:
        assert '.. versionadded:: ' in violation.__doc__


def test_violation_name(all_violations):
    """Ensures that all violations have `Violation` suffix."""
    for violation in all_violations:
        class_name = violation.__qualname__
        assert class_name.endswith('Violation'), class_name
