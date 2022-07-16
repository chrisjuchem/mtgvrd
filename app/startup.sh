#!/bin/bash

# Usage: ./startup.sh <target_dir> <launch_command>
# Should be run from the project root where alembic.ini and api/ are accessible.

# fail fast
set -e

# Update database
echo "Waiting for database connection..."
RESULT=1
ATTEMPTS=0
while true; do
  set +e
  OUTPUT=$(alembic current 2>&1)
  RESULT=$?
  set -e
  if [ $RESULT -eq 0 ]; then
    break
  fi

  ATTEMPTS=$((ATTEMPTS+1))
  if [ $ATTEMPTS -gt 5 ]; then
    echo "Maximum retries exceeded. Exiting."
    echo "Output of last attempt:"
    echo "$OUTPUT"
    exit 1
  fi

  echo "Not ready. Sleeping $ATTEMPTS second(s)."
  sleep $ATTEMPTS
done
echo "Connection ready. Running database migrations..."
alembic upgrade head
echo "Migrations complete."

# Move to target directory for launch command
cd ${COMMAND_DIR:-.}

# Run CMD (passed as args)
exec "$@"
