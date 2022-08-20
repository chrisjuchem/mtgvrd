#!/bin/bash

. env.sh --test

docker-compose down --volumes
docker-compose up -d

# Run tests in the test directory so that they can be found without providing any file names.
# This allows passing file names or `-k` patterns.
# Transform any provided relative file names to tests dir.
# DB logs can be re-enabled with --show-capture=log
# shellcheck disable=SC2001
CMD_DIR=app/tests ./app/startup.sh pytest --show-capture=no "$(echo "$@" | sed 's#^\(./\)\?app/tests/##g')"
EXIT_CODE=$?

docker-compose down

exit $EXIT_CODE
