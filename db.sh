#!/bin/bash

# Example Usages
#
# Interactive shell
# `./db.sh`
#
# Run a single SQL command
# `./db.sh -c 'select * from users order by last_login desc limit 2`
#
# Check the tables present in the test database
# `./db.sh --test -c '\dt`

. env.sh "$@"

if [[ "$1" == "--test" ]]; then
  shift
fi

docker exec -it $DB_CONTAINER_NAME psql -U $DB_USER -d $DB_NAME "$@"

# if you have psql installed locally you could use:
# PGPASSWORD=blacklotus psql -h 0.0.0.0 -p 5432 -U local_db_user -d mtgvrd -w
