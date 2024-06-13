.. _ondivi:

ondivi
------

``ondivi`` is a Python script filtering coding violations,
identified by static analysis, only for changed lines in a Git repo.

.. code:: bash

  pip install ondivi  # however we recommend to use `poetry`

Then you can integrate ``ondivi`` with your linter.
Below is an example of how to use ``ondivi`` with ``flake8``:

.. code:: bash

  flake8 script.py | ondivi

Optionally, you can configure ``ondivi`` to filter violations based on a
baseline commit or branch, and specify a custom format for parsing linter
messages.

.. code:: bash

  flake8 script.py | ondivi --baseline master --format "{filename}:{line_num:d}{other}"

Here is a detailed guide on how to set up ``ondivi`` for your project.

Baseline Concept
~~~~~~~~~~~~~~~~

When your project is old, you cannot just install and use a new linter because
your codebase will contain many violations. Some of them can be auto-formatted,
and some of them can be silenced. But, what if there are still too many of them
to fix right here and right now?

Let me introduce the ``baseline`` concept in ``ondivi``:

Specify the ``baseline`` commit or branch which contains your legacy code.
Run your linter and pipe its output to ``ondivi``:

.. code:: bash

  flake8 script.py | ondivi --baseline master

This will filter out violations present in the specified baseline, allowing
you to focus only on new violations.

Further Reading
~~~~~~~~~~~~~~~

For more information on ``ondivi`` and advanced usage, please refer to the
official repository:
`ondivi GitHub repository <https://github.com/blablatdinov/ondivi>`_

Support
~~~~~~~

``flakeheaven`` and ``flakehell`` are not supported because they rely on
internal ``flake8`` API, which can lead to compatibility issues as
``flake8`` evolves. In contrast, ``ondivi`` uses only the text output of
violations and the state of Git repository, making it more robust and
easier to maintain.

``ondivi`` is actively maintained and supported. If you encounter any issues or
have questions, please create an issue on the
`GitHub repository <https://github.com/blablatdinov/ondivi/issues>`_.
