#!/bin/bash

docker exec -it mtgvrd_db_1 psql -U local_db_user -d mtgvrd

# if you have psql installed locally you could use:
# PGPASSWORD=blacklotus psql -h 0.0.0.0 -p 5432 -U local_db_user -d mtgvrd -w
