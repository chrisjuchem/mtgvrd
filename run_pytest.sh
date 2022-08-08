#!/bin/bash

. env.sh --test

docker-compose down --volumes
docker-compose up -d

./app/startup.sh pytest app/tests "$@" # TODO handle individual files and names
EXIT_CODE=$?

docker-compose down

exit $EXIT_CODE