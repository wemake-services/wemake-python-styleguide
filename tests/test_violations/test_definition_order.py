import inspect


def _get_sorted_classes(classes):
    sorted_by_code = sorted(classes, key=lambda cl: cl.code)
    sorted_by_source = sorted(
        classes,
        key=lambda cl: inspect.findsource(cl)[1],
    )

    return sorted_by_code, sorted_by_source


def test_violation_source_order(all_module_violations):
    """Used to force violations order inside the source code."""
    for classes in all_module_violations.values():
        sorted_by_code, sorted_by_source = _get_sorted_classes(classes)

        assert sorted_by_code == sorted_by_source
