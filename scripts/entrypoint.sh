#!/bin/bash

# Passed args from GitHub Actions:
: "${INPUT_PATH:=$1}"
: "${INPUT_CWD:=$2}"
: "${INPUT_REPORTER:=$3}"
: "${INPUT_FILTER_MODE:=$4}"
: "${INPUT_FAIL_WORKFLOW:=$5}"

# Default values, needed because `Dockerfile` can be used directly:
# These values must match ones in `action.yml`!
: "${INPUT_PATH:='.'}"
: "${INPUT_CWD:='.'}"
: "${INPUT_REPORTER:='terminal'}"
: "${INPUT_FILTER_MODE:='added'}"
: "${INPUT_FAIL_WORKFLOW:=1}"

# Diagnostic output:
echo "Using 'path': $INPUT_PATH"
echo "Using 'cwd': $INPUT_CWD"
echo "Using 'reporter': $INPUT_REPORTER"
echo "Using 'filter_mode': $INPUT_FILTER_MODE"
echo "Using 'fail_workflow': $INPUT_FAIL_WORKFLOW"
echo 'flake8 --version:'
flake8 --version
echo '================================='
echo

cd "$INPUT_CWD" || exit 1

# Runs `flake8`, possibly with `reviewdog`:
if [ "$INPUT_REPORTER" == 'terminal' ]; then
  output=$(flake8 "$INPUT_PATH")
  status="$?"
elif [ "$INPUT_REPORTER" == 'github-pr-review' ] ||
     [ "$INPUT_REPORTER" == 'github-check' ] ||
     [ "$INPUT_REPORTER" == 'github-pr-check' ]; then
  # We will need this token for `reviewdog` to work:
  export REVIEWDOG_GITHUB_API_TOKEN="$GITHUB_TOKEN"

  # Running special version of `flake8` to match the `reviewdog` format:
  output=$(flake8 "$INPUT_PATH" --append-config='/action-config.cfg')
  echo "$output" | reviewdog -f=flake8 -reporter="$INPUT_REPORTER" -level=error
  # `reviewdog` does not fail with any status code, so we have to get dirty:
  # shellcheck disable=SC2319
  status=$(test "$output" = ''; echo $?)
else
  output="Invalid action reporter specified: $INPUT_REPORTER"
  status=1
fi

# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
delimiter="$(dd if=/dev/urandom bs=15 count=1 status=none | base64)"
# See: https://github.com/orgs/community/discussions/26288#discussioncomment-3876281
# shellcheck disable=SC2129
echo "output<<$delimiter" >> "$GITHUB_OUTPUT"
echo "$output" >> "$GITHUB_OUTPUT"
echo "$delimiter" >> "$GITHUB_OUTPUT"

echo '================================='
# Fail the build in case status code is not 0:
if [ "$status" != 0 ]; then
  echo "$output"
  echo "Process failed with the status code: $status"
  # Now, after reporting what the status code was, if `fail_workflow` is `1`,
  # fail the workflow. Otherwise, always `exit` with `0`.
  if [ "$INPUT_FAIL_WORKFLOW" = 1 ]; then
    exit "$status"
  else
    echo 'Since INPUT_FAIL_WORKFLOW is set, existing with 0'
    exit 0
  fi
fi
