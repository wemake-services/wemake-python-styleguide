GitHub Actions
--------------

.. image:: https://github.com/wemake-services/wemake-python-styleguide/workflows/wps/badge.svg
  :alt: GitHub Action badge
  :target: https://github.com/wemake-services/wemake-python-styleguide/actions

Good news: we ship pre-built GitHub Action with this project.

You can use it from the `GitHub Marketplace <https://github.com/marketplace/actions/wemake-python-styleguide>`_:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-services/wemake-python-styleguide

You can also specify any version instead of the ``latest`` tag.

Inputs
~~~~~~

.. rubric:: reporter

We support three reporting options:

- ``terminal`` (default one) when we just dump the output into Action's logs.
  Is the easiest one to setup, that's why we use it by default
- ``github-pr-review`` (recommended) when we use `inline comments <https://github.com/reviewdog/reviewdog#reporter-github-pullrequest-review-comment--reportergithub-pr-review>`_ inside code reviews
- ``github-pr-check`` when we use `GitHub PR Checks <https://github.com/reviewdog/reviewdog#reporter-github-checks--reportergithub-pr-check>`_ for the output
- ``github-check`` another way to use `GitHub Checks <https://github.com/reviewdog/reviewdog?tab=readme-ov-file#reporter-github-checks--reportergithub-check>`_ for the output

Take a note that ``github-check``, ``github-pr-review`` and ``github-pr-check``
requires ``GITHUB_TOKEN`` environment variable to be set.

Default reporter looks like so:

.. image:: https://raw.githubusercontent.com/wemake-services/wemake-python-styleguide/master/docs/_static/terminal.png

For example, that's how ``github-pr-reviews`` can be set up:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-services/wemake-python-styleguide
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
    uses: wemake-services/wemake-python-styleguide
    with:
      path: './your/custom/path'

.. rubric:: cwd

We also support custom ``cwd`` to be specified,
it will be used to ``cd`` into before any other actions.
It can be a custom subfolder with your configuration, etc.

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-services/wemake-python-styleguide
    with:
      cwd: './your/custom/path'

.. rubric:: fail_workflow

Option which can be set to ``false`` with ``fail_workflow: false`` not
to fail the workflow even if violations were found.

.. rubric:: filter_mode

Can be used to find only new violations and ignore old ones.
See https://github.com/reviewdog/reviewdog?tab=readme-ov-file#filter-mode

Outputs
~~~~~~~

We also support ``outputs`` from the spec, so you can later
pass the output of ``wemake-python-styleguide`` to somewhere else.

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-services/wemake-python-styleguide
  - name: Custom Action
    runs: echo "{{ steps.wemake-python-styleguide.outputs.output }}"
