SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy wemake_python_styleguide scripts
	poetry run flake8 .
	poetry run ruff format --check --diff
	poetry run ruff check --exit-non-zero-on-fix --diff
	poetry run lint-imports
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
