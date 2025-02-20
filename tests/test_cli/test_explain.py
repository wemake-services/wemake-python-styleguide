"""Integration testing of wps explain command."""

import subprocess

import pytest


def _popen_in_shell(args: str) -> tuple[subprocess.Popen, str, str]:
    """Run command in shell."""
    # shell=True is needed for subprocess.Popen to
    # locate the installed wps command.
    process = subprocess.Popen(  # noqa: S602 (insecure shell=True)
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    stdin, stdout = process.communicate()
    return process, stdin, stdout


def test_command(snapshot):
    """Test that command works and formats violations as expected."""
    process, stdout, stderr = _popen_in_shell('wps explain WPS123')
    assert process.returncode == 0, (stdout, stderr)
    assert stdout == snapshot
    assert not stderr


@pytest.mark.parametrize(
    'command',
    [
        'wps explain 10000',
        'wps explain NOT_A_CODE',
        'wps explain WPS10000',
    ],
)
def test_command_on_not_found(command, snapshot):
    """Test command works when violation code is wrong."""
    process, stdout, stderr = _popen_in_shell(command)
    assert process.returncode == 1, (stdout, stderr)
    assert not stdout
    assert stderr == snapshot


def test_no_command_specified(snapshot):
    """Test command displays error message when no subcommand provided."""
    process, stdout, stderr = _popen_in_shell('wps')
    stdout, stderr = process.communicate()
    assert process.returncode != 0, (stdout, stderr)
    assert not stdout
    assert stderr == snapshot
