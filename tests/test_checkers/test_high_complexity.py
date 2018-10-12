# -*- coding: utf-8 -*-

import subprocess


def test_too_many_arguments_in_fixture(absolute_path):
    """
    End-to-End test to check arguments count.

    It is required due to how 'function_type' parameter
    works inside 'flake8'.

    Otherwise it is not set, unit tests can not cover `is_method` correctly.
    """
    filename = absolute_path('fixtures', 'config', 'wrong_arguments.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z211') == 4


def test_too_many_arguments_in_lambda_fixture(absolute_path):
    """
    End-to-End test to check arguments count in lambda.

    It is required due to how 'function_type' parameter
    works inside 'flake8'.

    Otherwise it is not set, unit tests can not cover `is_method` correctly.
    """
    filename = absolute_path('fixtures', 'config', 'wrong_arguments_lambda.py')
    process = subprocess.Popen(
        ['flake8', '--select', 'Z', filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, _ = process.communicate()

    assert stdout.count(b'Z211') == 5
