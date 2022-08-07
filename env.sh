#!/bin/bash

. venv/bin/activate

export APP_PORT=5000

export DB_USER="local_db_user"
export DB_HOST="0.0.0.0"
export DB_PORT="5432"
export DB_NAME="mtgvrd"

export DISCORD_CLIENT_ID="1002261974698180748"
export DISCORD_AUTHORIZE_URL="https://discord.com/api/oauth2/authorize"
export DISCORD_ACCESS_TOKEN_URL="https://discord.com/api/oauth2/token"
export DISCORD_USER_INFO_URL="https://discord.com/api/users/@me"


if [[ "$1" == "--test" ]]; then
  export TEST_ENVIRONMENT=1
  export COMPOSE_FILE="docker-compose.test.yaml"
  export COMPOSE_PROJECT_NAME="test"
  export DB_CONTAINER_NAME=test_db_1
  export export DB_PORT=5444
else
  unset TEST_ENVIRONMENT
  unset COMPOSE_FILE
  unset COMPOSE_PROJECT_NAME
  export DB_CONTAINER_NAME=mtgvrd_db_1
  # DB_PORT set above
fi



if [[ -f "secrets.sh" ]]; then
  . ./secrets.sh
fi
