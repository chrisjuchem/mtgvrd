# mtgvrd

## Useful commands for development

- Get Started
  - `. first_time_setup.sh` - Perform first-time setup for a new env. Note: this should be sourced
    instead of run directly.
  - `. venv/bin/activate` - Start using the virtual environment
  - Create `app/sevrer/secrets.json` with secret values.
  - `./launch_dev.sh` - Start the db, api, and client in parallel
  - `. env.sh` - Source local dev environment variables into your shell
  - `. env.sh --test` - Source local dev environment variables for testing into your shell
  - `deactivate` - Stop using the virtual environment
- Application
- - `docker-compose build` - Build the image for the local db container
  - `./start-app.sh` - Start the app with flask dev server, including running the latest migrations.
  - `./start-app.sh -g` - Start the app with gunicorn (production config), including running the latest migrations.
  - `yarn --cwd app/client start` - Start the React dev server to serve frontend with hotloading
  - `yarn --cwd app/client build` - Create build assets from the react app to be served by flask
- Database
  - `docker-compose up -d` - Start the postgres database in the background
  - `./db.sh` - Connect to the local database
  - `docker-compose down` - Stop the local database
  - `docker-compose down --volumes` - Nuke the local db. It will need to be rebuilt.
- Database migrations
  - `alembic revision --autogenerate -m "migration name"` - Create a new migration that will bring
    the database up to the current state of the models in source code.
  - `alembic upgrade head` - Apply all migrations to the local database
  - `alembic downgrade -1` - Revert the last migration. Important to do before deleting a migration
    if you want to regenerate it.
