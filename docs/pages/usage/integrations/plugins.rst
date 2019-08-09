Plugins and Hooks
-----------------

We leverage all the existing ``flake8``
`infrastructure <https://github.com/DmytroLitvinov/awesome-flake8-extensions>`_
and tools.
There are different integrations for your workflow.

Plugins
~~~~~~~

There are a lot of specific plugins that are not included,
because they are, well, specific:

- `flake8-pytest <https://github.com/vikingco/flake8-pytest>`_
- `flake8-django <https://github.com/rocioar/flake8-django>`_
- `flake8-scrapy <https://github.com/stummjr/flake8-scrapy>`_
- `pandas-vet <https://github.com/deppen8/pandas-vet>`_

Hooks
~~~~~

Hooks are 3rd-party apps and services
that run ``flake8`` on different occasions:

- `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ to run style checks
  alongside with tests
- `pre-commit <https://pre-commit.com/>`_ to run ``flake8``
  before all commits locally
- `pronto-flake8 <https://github.com/scoremedia/pronto-flake8>`_ to post
  inline-comments with violations during code-review inside your CI
