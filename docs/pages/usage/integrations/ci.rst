CI
--

This guide shows how to use ``flake8`` inside your ``CI``.

travis
~~~~~~

Here's the minimal configuration required
to set up ``wemake-python-styleguide``, ``flake8``, ``travis`` up and running:

1. Learn how to `build python projects with travis <https://docs.travis-ci.com/user/languages/python/>`_
2. Copy this configuration into your ``.travis.yml``:

  .. code:: yaml

    dist: xenial
    language: python
    python: 3.7

    install: pip install wemake-python-styleguide
    script: flake8 .

You can also have some inspiration in our own `.travis.yml <https://github.com/wemake-services/wemake-python-styleguide/blob/master/.travis.yml>`_
configuration file.

Gitlab CI
~~~~~~~~~

Setting up ``GitlabCI`` is also easy:

1. Learn how `Gitlab CI works <https://docs.gitlab.com/ee/ci/>`_
2. Copy this configuration into your ``.gitlab-ci.yml``:

  .. code:: yaml

    image: python3.7
    test:
      before_script: pip install wemake-python-styleguide
      script: flake8 .

Examples:

- ``GitlabCI`` + ``python`` `official template <https://gitlab.com/gitlab-org/gitlab-ce/blob/master/lib/gitlab/ci/templates/Python.gitlab-ci.yml>`_
- ``django`` + ``docker`` + ``GitlabCI`` `template <https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/.gitlab-ci.yml>`_
