#!/bin/bash

. env.sh

echo Starting Flask app on port $APP_PORT

if [ "$1" == "-g" ] ; then
    export GUNICORN_THREADS=2 #TODO: tune
    export GUNICORN_WORKERS=2
    echo "Lauching prod configuration with gunicorn"
    ./app/startup.sh gunicorn app.server.app:app --config app/server/gunicorn_conf.py
else
    export FLASK_APP=app.server.app
    export FLASK_ENV=development
    echo "Lauching dev configuration"
    ./app/startup.sh flask run --no-debugger -p $APP_PORT
fi
