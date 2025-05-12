#!/bin/bash
COVERAGE_THRESHOLD=60

coverage run -m pytest
coverage report | tee coverage.txt
COVERAGE=$(coverage report | tail -1 | awk '{print $NF}' | sed 's/%//')

if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
    echo "Test coverage $COVERAGE% is below threshold of $COVERAGE_THRESHOLD%"
    exit 1
fi
