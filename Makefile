SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	mypy wemake_python_styleguide
	flake8 .
	autopep8 -r . --diff --exclude=./tests/fixtures/** --exit-code
	xenon --max-absolute B --max-modules A --max-average A wemake_python_styleguide
	lint-imports
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
test: lint unit package
