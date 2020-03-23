from os import chmod

import pytest

_TEMP_FOLDER = 'tmp'
_MODE_EXECUTABLE = 0o755
_MODE_NON_EXECUTABLE = 0o644


@pytest.fixture()
def make_file(tmp_path):
    """Fixture to make a temporary executable or non executable file."""
    def factory(
        filename: str,
        file_content: str,
        *,
        is_executable: bool = False,
    ) -> str:
        temp_folder = tmp_path / _TEMP_FOLDER
        temp_folder.mkdir(exist_ok=True)
        test_file = temp_folder / filename
        file_mode = _MODE_EXECUTABLE if is_executable else _MODE_NON_EXECUTABLE

        test_file.write_text(file_content)
        chmod(test_file.as_posix(), file_mode)

        return test_file.as_posix()
    return factory
