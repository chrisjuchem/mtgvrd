#!/bin/bash

#This file must be sourced or run `. venv/bin/activate` afterwards

python3.8 -m virtualenv venv
. venv/bin/activate

pip3 install -r requirements.txt
(cd app/client && yarn)

echo "run \`. venv/bin/activate\` to begin working"