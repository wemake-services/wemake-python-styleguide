import subprocess


def test_invalid_options(absolute_path):
    """End-to-End test to check option validation works."""
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'WPS',
            '--max-imports',
            '-5',  # should be positive
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 1
    assert 'ValueError' in stderr


def test_invalid_domain_names_options(absolute_path):
    """End-to-End test to check domain names options validation works."""
    process = subprocess.Popen(
        [
            'flake8',
            '--isolated',
            '--select',
            'WPS',
            # values from `allowed-domain-names` cannot intersect with
            # `--forbidden-domain-names`
            '--allowed-domain-names',
            'item,items,handle,visitor',
            '--forbidden-domain-names',
            'handle,visitor,node',
            absolute_path('fixtures', 'noqa.py'),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding='utf8',
    )
    _, stderr = process.communicate()

    assert process.returncode == 1
    assert 'ValueError' in stderr
    assert 'handle' in stderr
    assert 'visitor' in stderr
