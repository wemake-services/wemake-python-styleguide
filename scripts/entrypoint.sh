#!/bin/bash
set -e

# Runs flake8:
output=$(flake8 "$1")

# Outputs the result to the console:
echo "$output"

# Sets the output variable for Github Action API:
echo ::set-output name=output::$output
