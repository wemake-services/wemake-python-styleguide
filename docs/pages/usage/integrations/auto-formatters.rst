Auto-formatters
---------------

List of supported tools.


ruff
~~~~

Fully supported.
You can run ``ruff check && ruff format`` and there
should be no conflicts with ``WPS`` at all.

But, ``wemake-python-styleguide`` can and will find additional
problems that ``ruff`` missed.


isort
~~~~~

We support ``isort``, but we recommend to use ``ruff`` instead.
See https://docs.astral.sh/ruff/rules/#isort-i


black
~~~~~

Is supported since ``1.0.0``, but we recommend to use ``ruff format`` instead.
