#!/bin/bash

function RunTests {
    docker-compose run app sh -c "python manage.py test"
}

function RunLint {
    docker-compose run app sh -c "flake8"
}

function RunTestAndLint {
    docker-compose run app sh -c "python manage.py test && flake8"
}

###

for arg in "$@"; do
  if [[ "$arg" = -t ]] || [[ "$arg" = --run-test ]]; then
    ARG_RUN_TEST=true
  fi
  if [[ "$arg" = -l ]] || [[ "$arg" = --run-lint ]]; then
    ARG_RUN_LINT=true
  fi
  if [[ "$arg" = -a ]] || [[ "$arg" = --run-all ]]; then
    ARG_RUN_ALL=true
  fi
done

###

if [[ "$ARG_RUN_TEST" = true ]]; then
  RunTests
fi

if [[ "$ARG_RUN_LINT" = true ]]; then
  RunLint
fi

if [[ "$ARG_RUN_ALL" = true ]]; then
  RunTests
  RunLint
fi