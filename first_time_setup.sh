#!/bin/bash

#This file must be sourced or you must run `. venv/bin/activate` afterwards

python3.8 -m virtualenv venv
. venv/bin/activate

pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
(cd app/client && yarn)
sudo npm i -g nf

pre-commit install

echo
echo "+=====================================================================+"
echo "| Run \`. venv/bin/activate\` to begin working if this was not sourced! |"
echo "+=====================================================================+"
