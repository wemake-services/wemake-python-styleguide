import subprocess

from wemake_python_styleguide.version import pkg_name, pkg_version


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    pkg_qualifier = pkg_name.replace('_', '-')
    assert pkg_qualifier
    assert pkg_version

    output_text = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf8',
    )
    output_text = output_text.replace('_', '-').replace('\n', '')

    assert pkg_qualifier in output_text
    assert pkg_version in output_text


def test_call_flake8_help():
    """Checks that module is registered and visible in the help."""
    output_text = subprocess.check_output(
        ['flake8', '--help'],
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf8',
    )

    assert pkg_name
    assert pkg_name in output_text or pkg_name.replace('_', '-') in output_text
