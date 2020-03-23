import os

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
        os.chmod(test_file.as_posix(), file_mode)

        return test_file.as_posix()
    return factory


@pytest.fixture(scope='session')
def read_file(absolute_path):
    """Fixture to get the file contents."""
    def factory(filename: str) -> str:
        with open(filename) as file_obj:
            return file_obj.read()
    return factory


@pytest.fixture(scope='session')
def absolute_path():
    """Fixture to create full path relative to `contest.py` inside tests."""
    def factory(*files: str):
        dirname = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(dirname, *files)
    return factory
