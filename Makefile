SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	mypy wemake_python_styleguide
	flake8 .
	autopep8 -r . --diff --exclude=./tests/fixtures/** --exit-code
	lint-imports
	doc8 -q docs

.PHONY: unit
unit:
	pytest

.PHONY: package
package:
	poetry check
	pip check
	safety check --bare --full-report

.PHONY: test
test: lint unit package
