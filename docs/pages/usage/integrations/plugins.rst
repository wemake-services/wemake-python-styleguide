Plugins and hooks
-----------------

We leverage all the existing ``flake8``
`infrastructure <https://github.com/DmytroLitvinov/awesome-flake8-extensions>`_
and tools.
There are different integrations for your workflow.

Plugins
~~~~~~~

There are a lot of specific plugins that are not included,
because they are, well, specific:

- `flake8-pytest-style <https://github.com/m-burst/flake8-pytest-style>`_
- `flake8-django <https://github.com/rocioar/flake8-django>`_
- `flake8-scrapy <https://github.com/stummjr/flake8-scrapy>`_
- `pandas-vet <https://github.com/deppen8/pandas-vet>`_
- `flake8-SQL <https://pypi.org/project/flake8-SQL/>`_
- `flake8-annotations <https://github.com/python-discord/flake8-annotations>`_
- `flake8-logging-format <https://github.com/globality-corp/flake8-logging-format>`_
- `flake8-coding <https://github.com/tk0miya/flake8-coding>`_
- `flake8-spellcheck <https://github.com/MichaelAquilina/flake8-spellcheck>`_

Hooks
~~~~~

Hooks are 3rd-party apps and services
that run ``flake8`` on different occasions:

- `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ to run style checks
  alongside with tests
- `pre-commit <https://pre-commit.com/>`_ to run ``flake8``
  before all commits locally

  - Note that since the default ``flake8`` used by ``pre-commit`` does not have
    ``wemake`` plugin, we have to ask ``pre-commit`` to run local ``flake8``
    that is installed via ``wemake``. A sample config for
    ``.pre-commit-config.yaml``:

  .. code:: yaml

    repos:
    -   repo: local
        hooks:
        -   id: flake8
            name: flake8
            description: wemake-python-styleguide enforcement
            entry: flake8
            args: ["--config=setup.cfg"]
            language: python
            types: [python]

- `pronto-flake8 <https://github.com/scoremedia/pronto-flake8>`_ to post
  inline-comments with violations during code-review inside your CI
- Directly modify git pre-commit hook without third party app or service.

  - Open ``<your_local_repo>/.git/hooks/pre-commit.sample`` (git runs this
    script after one calls ``git commit``. If this script exits with code 1,
    commit would fail)
  - Add the following code **before** the one checking for whitespace errors.

  .. code:: bash

    # Your added code to run wemake-python-styleguide. Add this before
    # the whitespace error lines
    flake8 .
    if [ $? -ne 0 ]
    then
     echo "Please fix the ERRORS and commit again."
     exit 1
    fi

    # If there are whitespace errors, print the offending file names and fail.
    exec git diff-index --check --cached $against --

  - Save and rename the file from ``pre-commit.sample`` to ``pre-commit``
