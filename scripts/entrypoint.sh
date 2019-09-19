#!/bin/bash

# Diagnostic output for the passed path:
echo "Linting path: $1"

# Runs flake8:
output=$(flake8 "$1")

# Sets the output variable for Github Action API:
echo ::set-output name=output::$output

# Fail the build in case there's any output (means there are violations):
if [[ "$output" ]]; then
  echo "$output"
  exit 1
fi
