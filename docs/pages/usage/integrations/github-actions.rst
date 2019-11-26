Github Actions
--------------

.. image:: https://github.com/wemake-services/wemake-python-styleguide/workflows/wps/badge.svg
  :alt: Github Action badge
  :target: https://github.com/wemake-services/wemake-python-styleguide/actions

Good news: we ship pre-built Github Action with this project.

You can use it from the `Github Marketplace <https://github.com/marketplace/actions/wemake-python-styleguide>`_:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest

You can also specify any version
starting from ``0.12.5`` instead of the ``latest`` tag.
You can also specify to leave inline PR comments
and PR summary review starting from ``0.13.1`` version.

Inputs
~~~~~~

.. rubric:: reporter

We support three reporting options:

- ``terminal`` (default one) when we just dump the output into Action's logs.
  Is the easiest one to setup, that's why we use it by default
- ``github-pr-review`` (recommended) when we use `inline comments <https://github.com/reviewdog/reviewdog#reporter-github-pullrequest-review-comment--reportergithub-pr-review>`_ inside code reviews
- ``github-pr-check`` when we use `Github Checks <https://github.com/reviewdog/reviewdog#reporter-github-checks--reportergithub-pr-check>`_ for the output

Take a note that ``github-pr-review`` and ``github-pr-check`` requires
``GITHUB_TOKEN`` environment variable to be set.

Default reporter looks like so:

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/terminal.png

For example, that's how ``github-pr-reviews`` can be set up:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest
    with:
      reporter: 'github-pr-review'
    env:
      GITHUB_TOKEN: ${{ secrets.github_token }}

That's how the result will look like:

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/reviewdog.png

.. rubric:: path

We also support custom ``path`` to be specified:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest
    with:
      path: './your/custom/path'

Outputs
~~~~~~~

We also support ``outputs`` from the spec, so you can later
pass the output of ``wemake-python-styleguide`` to somewhere else.

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest
  - name: Custom Action
    runs: echo "{{ steps.wemake-python-styleguide.outputs.output }}"
