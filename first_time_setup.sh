#!/bin/bash

#This file must be sourced or you must run `. venv/bin/activate` afterwards

set -e

python3.8 -m virtualenv venv
. venv/bin/activate

pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
yarn --cwd app/client
yarn global add foreman

pre-commit install

echo
echo "+==========================================================+"
echo "| Run \`. env.sh\` to begin working if this was not sourced! |"
echo "+==========================================================+"
