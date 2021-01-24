Internal Docs
=============

Here you can find:

1. How our development process works
2. How to contribute to the project
3. How to write new rules
4. How our internal API looks like

This information will also be helpful
if you would like to create your own ``flake8`` plugin.

How to read this documentation
------------------------------

You will need to start from the :ref:`glossary <glossary>`
where we define the terms for this project.

Then move to the :ref:`contributing <contributing>` guide
where we specify all technical details about our workflow and tools.

Then you will be ready
to dive into our :ref:`"Creating a new rule tutorial" <tutorial>`.

And finally you will need to go through the API reference
to cover specific technical questions you will encounter.


Philosophy
----------

1. Done is better than perfect
2. However, we pursue perfect software
3. False negatives over false positives
4. If you cannot sustain your promise - do not promise
5. Code must be written for people to read,
   and only incidentally for machines to execute
6. Value consistency over syntax-ish readability
7. Consistent code is more readable than inconsistent
8. Do not force people to choose, they will make mistakes
9. Made choices must be respected


Overview
--------

This schema should give you a brief overview of what is happening inside
our linter. This is a very simplified architecture that will help you
to understand how all components are bound together.

.. mermaid::
   :caption: Architecture overview.

   sequenceDiagram
      participant flake8
      participant Checker
      participant Transformation
      participant Visitor
      participant Violation

      flake8->>Checker: flake8 runs our checker alongside with other plugins
      Checker->>Transformation: Checker asks to perform different ast transformations before we actually start doing anything
      Checker->>Visitor: Checker runs all visitors that it is aware of
      Visitor->>Violation: Visitors raise violations when they find bad code
      Violation-->>flake8: Raised violations are shown to user by flake8

We use a `layered architecture <https://import-linter.readthedocs.io/>`_
that follows this contract:

.. literalinclude :: ../../../.importlinter
   :language: ini

Contributing
------------

.. toctree::
  :maxdepth: 2
  :caption: This section will help you to know all
    the tools and terms we are using.

  glossary.rst
  contributing.rst
  debugging.rst


Creating a new rule
-------------------

.. toctree::
  :maxdepth: 2
  :caption: This tutorial will guide you through the whole process
    of creating new rules for this linter.

  tutorial.rst


API Reference
-------------

.. toctree::
  :maxdepth: 1
  :caption: Raw technical information with interface and types declarations,
    featuring architecture and composition of classes.

  checker.rst
  visitors.rst
  violations.rst
  transformations.rst
  types.rst
  constants.rst
  formatter.rst
