import subprocess

from wemake_python_styleguide.version import pkg_name, pkg_version


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    output_text = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf8',
    )

    assert pkg_name
    assert pkg_version

    assert pkg_name in output_text or pkg_name.replace('_', '-') in output_text
    assert pkg_version in output_text


def test_call_flake8_help():
    """Checks that module is registered and visible in the help."""
    output_text = subprocess.check_output(
        ['flake8', '--help'],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf8',
    )

    assert pkg_name
    assert pkg_name in output_text or pkg_name.replace('_', '-') in output_text
