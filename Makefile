SHELL:=/usr/bin/env bash

.PHONY: check-format
check-format:
	autopep8 -r . --diff --exclude=./tests/fixtures/** --exit-code

.PHONY: lint
lint:
	mypy wemake_python_styleguide
	flake8 .
	layer-lint --quiet wemake_python_styleguide
	poetry run doc8 -q docs

.PHONY: unit
unit:
	pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --bare --full-report

.PHONY: test
test: lint check-format unit package
