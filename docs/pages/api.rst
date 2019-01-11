Internal Docs
=============

Here you can find:

1. How our development process works
2. How to contribute to the project
3. How to write new rules
4. How our internal API looks like

This information will also be helpful
if you would like to create our own ``flake8`` plugin.

How to read this documentation
------------------------------

You will need to start from the :ref:`glossary <glossary>`
where we define the terms for this project.

Then move to the :ref:`contributing <contributing>` guide
where we specify all technical details about our workflow and tools.

And finally you will need to go through the API reference.


Philosophy
----------

1. Done is better than perfect
2. False negatives over false positives
3. If you can not sustain your promise - do not promise
4. Code is written to be read
5. Consistency over syntatic readability
6. Consistent code is more readable than inconsistent
7. Do not force people to chose, they will make mistakes
8. Choice must be respected


Overview
--------

This schema should give you a brief overview of what is happening inside
our linter. This is a very simplified architecture that will help you
to understand how all components are bound together.

.. mermaid::
   :caption: Architecture overview

   sequenceDiagram
      participant flake8
      participant Checker
      participant Transformation
      participant Visitor
      participant Violation

      flake8->>Checker: flake8 runs our checker alongside with other plugins
      Checker->>Transformation: Checker asks to perform different ast transformations before we actually start doing anything
      Checker->>Visitor: Checker runs all visitors that are it is aware of
      Visitor->>Violation: Visitors raise violations when they find bad code
      Violation-->>flake8: Raised violations are shown to user by flake8

Contributing
------------

.. toctree::
  :maxdepth: 2

  glossary.rst
  contributing.rst

API Reference
-------------

.. toctree::
  :maxdepth: 2

  checker.rst
  visitors/base.rst
  violations/base.rst
