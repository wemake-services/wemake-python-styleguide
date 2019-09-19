Github Actions
--------------

.. image:: https://github.com/wemake-services/wemake-python-styleguide/workflows/wps/badge.svg
  :alt: Github Action badge
  :target: https://github.com/wemake-services/wemake-python-styleguide/actions

Good news: we ship pre-built Github Action with this project.

You can use it from the Github Marketplace:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest

You can also specify any version
starting from ``0.12.5`` instead of the ``latest`` tag.

Inputs
~~~~~~

We also support custom path to be specified:

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest
    with:
      path: './your/custom/path'

Outputs
~~~~~~~

We also support ``outputs`` from the spec, so you can later
pass the output of ``wemake-python-styleguide`` to somewhere else.
For example to `reviewdog <https://github.com/reviewdog/reviewdog>`_ app.

.. code:: yaml

  - name: wemake-python-styleguide
    uses: wemake-python-styleguide@latest
    with:
      path: './your/custom/path'
  - name: Custom reviewdog Action
    runs: echo "{{ steps.wemake-python-styleguide.outputs.output }}" | reviewdog -f pep8

Note, that Github Actions are currently in beta.
