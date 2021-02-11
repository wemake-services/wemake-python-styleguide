import pytest


@pytest.fixture(scope='session')
def compile_code():
    """
    Compiles given string to Python's AST.

    We need to compile to check some syntax features
    that are validated after the ``ast`` is processed:
    like double arguments or ``break`` outside of loops.
    """
    def factory(code_to_parse: str) -> None:
        compile(code_to_parse, '<filename>', 'exec')  # noqa: WPS421
    return factory
