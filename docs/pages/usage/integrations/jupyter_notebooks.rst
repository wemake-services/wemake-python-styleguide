.. _jupyter_notebooks:

Jupyter Notebooks
-----------------

``flake8`` does not run on Jupyter Notebooks out-of-the-box. However, there exist projects
such as `nbqa <https://github.com/nbQA-dev/nbQA>`_ and
`flake8-nb <https://github.com/s-weigand/flake8-nb>`_ which allow you to do so.

Due to some error/warning codes not applying naturally to Jupyter Notebooks
(e.g. "missing module docstring"), it may be a good idea to ignore some of them,
for example by running:

.. code:: bash

    $ nbqa flake8 notebook.ipynb --extend-ignore=NIP102,D100,E302,E305,E703,WPS102,WPS114

For example, if we have a file ``notebook.ipynb``

.. image:: https://raw.githubusercontent.com/MarcoGorelli/wemake-python-styleguide/issue-1704/docs/_static/notebook.png

we can run this project on this as follows:

.. image:: https://raw.githubusercontent.com/MarcoGorelli/wemake-python-styleguide/issue-1704/docs/_static/notebook_terminal.png
