#!/bin/bash

# Diagnostic output for the passed path:
echo "Linting path: $1"
echo '================================='
echo

# Runs flake8:
output=$(flake8 "$1")
status="$?"

# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
echo "::set-output name=output::$output"
echo '================================='
echo

# Fail the build in case status code is not 0:
if [[ "$status" != 0 ]]; then
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi
