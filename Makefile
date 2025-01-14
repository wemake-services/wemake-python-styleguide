SHELL:=/usr/bin/env bash

.PHONY: format
format:
	poetry run ruff format
	poetry run ruff check

.PHONY: lint
lint:
	poetry run ruff check --exit-non-zero-on-fix --diff
	poetry run ruff format --check --diff
	poetry run flake8 .
	poetry run mypy wemake_python_styleguide scripts
	poetry run lint-imports
	poetry run python3 scripts/check_generic_visit.py wemake_python_styleguide/visitors/ast

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	# TODO: re-enable when poetry@2.0 support will be fixed
	# poetry run poetry check
	poetry run pip check

.PHONY: test
test: lint unit package
