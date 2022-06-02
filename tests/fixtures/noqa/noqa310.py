"""
Here we list errors that are specific for python3.10 and further versions.

Please, do not add general violations here.
"""


def function_with_unions(
    arg1: Union[int, str],   # noqa: WPS473
    arg2: Optional[int],  # noqa: WPS473
) -> None:
    """Docstring."""

