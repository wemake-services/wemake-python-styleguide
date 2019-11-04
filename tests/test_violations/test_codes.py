# -*- coding: utf-8 -*-


def test_all_unique_violation_codes(all_violations):
    """Ensures that all violations have unique violation codes."""
    codes = []
    for violation in all_violations:
        codes.append(int(violation.code))

    assert len(set(codes)) == len(all_violations)


def test_all_violations_correct_numbers(all_module_violations):
    """Ensures that all violations has correct violation code numbers."""
    assert len(all_module_violations) == 8

    for index, module in enumerate(all_module_violations.keys()):
        code_number = index * 100
        for violation_class in all_module_violations[module]:
            assert (
                code_number <= violation_class.code <= code_number + 100 - 1
            ), violation_class.__qualname__


def test_violations_start_zero(all_module_violations):
    """Ensures that all violations start at zero."""
    for index, module in enumerate(all_module_violations.keys()):
        starting_code = min(
            violation_class.code
            for violation_class in all_module_violations[module]
        )
        assert starting_code == index * 100


def test_no_holes(all_module_violations):
    """Ensures that there are no off-by-one errors."""
    for module in all_module_violations.keys():
        previous_code = None

        for violation_class in all_module_violations[module]:
            if previous_code is not None:
                diff = violation_class.code - previous_code
                assert diff == 1 or diff > 2, violation_class.__qualname__
            previous_code = violation_class.code
