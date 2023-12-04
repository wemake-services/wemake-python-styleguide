SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy wemake_python_styleguide scripts
	poetry run flake8 .
	poetry run autopep8 -r . --diff --exclude=./tests/fixtures/** --exit-code
	poetry run lint-imports
	poetry run doc8 -q docs
	poetry run python3 scripts/check_generic_visit.py wemake_python_styleguide/visitors/ast

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry run poetry check
	poetry run pip check

.PHONY: test
test: lint unit package
