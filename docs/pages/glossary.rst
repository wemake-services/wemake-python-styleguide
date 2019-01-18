.. _glossary:

Glossary
========

First of all, we should speak the same language.
Here we collect all the specific terms that are used in this project.

.. glossary::

  rule
    Some decision that we have made regarding our ``python`` code.

    Rules can say how we do thing or how we do not do things.
    Each rule is represented with a :term:`violation`.

  plugin
    An application developed following `official guides <flake8.pycqa.org/en/latest/plugin-development/index.html>`_
    and compatible with ``flake8``.

  wemake_python_styleguide
    ``flake8`` :term:`plugin`.

    Represents a set of :term:`rules <rule>` of how we do write
    ``python`` code in `wemake.services <https://wemake.services>`_.

  checker
    A class compatible with ``flake8`` used as a :term:`plugin` entry point.

    This class runs all :term:`visitors <visitor>` that exist
    in our application.

    Technical documentation about the :ref:`checker` is available.

  transformation
    A way we change existing ``ast`` nodes.

    We can add properties, fix errors, delete or replace some nodes.
    Some of the reasons for these actions are: developer experience,
    simplicity, consistency across different versions, bug-fixing.

  visitor
    An object that goes through set of ``ast``, ``tokenize``, or other
    nodes to find :term:`violation` of our :term:`rules <rule>`.

    Technical documentation about
    the :ref:`visitors` is available.

  preset
    A collection of :term:`visitors <visitor>`.

    We use this concept to be able to pass multiple :term:`visitor` classes
    into the :term:`checker` to be run.

  violation
    Stylistic or semantic error that goes against our :term:`rules <rule>`.

    We count each violation definition
    as a strict rule: how should we behave in different situations.

    Each violation has its own reasoning, solution, and code examples.
    Some violations can be configured,
    some violations contains related constants.

    Technical documentation about
    the :ref:`violations` is available.
