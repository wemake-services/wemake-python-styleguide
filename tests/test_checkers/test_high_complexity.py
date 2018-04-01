# -*- coding: utf-8 -*-

import subprocess


def test_too_many_variables_in_fixture(absolute_path):
    """End-to-End test to check variables count."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_variables.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS150') == 2


def test_too_many_arguments_in_fixture(absolute_path):
    """End-to-End test to check arguments count."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_arguments.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS151') == 4


def test_too_many_returns_in_fixture(absolute_path):
    """End-to-End test to check returns count."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_returns.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS153') == 1


def test_too_many_expressions_in_fixture(absolute_path):
    """End-to-End test to check expressions count."""
    filename = absolute_path('fixtures', 'complexity', 'wrong_expressions.py')
    process = subprocess.Popen(
        ['flake8', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'WPS154') == 1
