# -*- coding: utf-8 -*-


def test_all_unique_violation_codes(all_violations):
    """Ensures that all violations have unique violation codes."""
    codes = []
    for violation in all_violations:
        codes.append(int(violation.code))

    assert len(set(codes)) == len(all_violations)


def test_all_violations_correct_numbers(all_module_violations):
    """Ensures that all violations has correct violation code numbers."""
    assert len(all_module_violations) == 4

    for index, module in enumerate(all_module_violations.keys()):
        classes = all_module_violations[module]
        code_number = (index + 1) * 100
        for violation_class in classes:
            assert code_number <= violation_class.code <= code_number + 100 - 1
