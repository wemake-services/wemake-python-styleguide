.. _glossary:

Glossary
========

.. glossary::

   wemake_python_styleguide
      Set of rules of how we write ``python`` code
      that is used together in `wemake.services <https://wemake.services>`_.

   checker
      ``flake8`` plugin compatible class that is used as an entrypoint.
      Entrypoint and violation codes are defined in ``pyproject.toml``.
      This class runs all visitors that exist in our styleguide.

   visitor
      An object that goes through set of ``ast``, ``tokenize``, or other
      nodes to find violation of our rules.

   violation
      Stylistic or sematic error. We count each violation definition as a rule.
      Each violation has its own reasoning, solution, and code examples.
      Some violations can be configured,
      some violations contains related constants.
