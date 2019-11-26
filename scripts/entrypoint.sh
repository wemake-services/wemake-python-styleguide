#!/bin/bash

# Setting up:
export REVIEWDOG_GITHUB_API_TOKEN="$GITHUB_TOKEN"

# Diagnostic output for the passed path:
flake8 --version
echo "Linting path: $INPUT_PATH"
echo '================================='
echo

# Runs flake8, possibly with reviewdog:
if [ "$INPUT_REPORTER" == 'terminal' ]; then
  output=$(flake8 "$INPUT_PATH")
elif [ "$INPUT_REPORTER" == 'github-pr-review' ] ||
     [ "$INPUT_REPORTER" == 'github-pr-check' ]; then
  output=$(flake8 "$INPUT_PATH" --append-config='/action-config.cfg')
  echo "$output" | reviewdog -f='pep8' -reporter="$INPUT_REPORTER"
fi
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
