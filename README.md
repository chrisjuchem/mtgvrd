# mtgvrd

## Useful commands for development

- Dev environment
  - `. first_time_setup.sh` - Perform first-time setup for a new env. Note: this should be sourced
    instead of run directly.
  - `docker-compose up -d` - Start the postgres database in the background
  - `./db.sh` - Connect to the local database
  - `docker-compose down` - Stop the local database
  - `. venv/bin/activate` - Start using the virtual environment
  - `deactivate` - Stop using the virtual environment
- Application
  - `./start-app.sh` - Start the app with flask dev server, including running the latest migrations.
  - `./start-app.sh -g` - Start the app with gunicorn (production config), including running the latest migrations.
- Database migrations
  - `alembic revision --autogenerate -m "migration name"` - Create a new migration that will bring
    the database up to the current state of the models in source code.
  - `alembic upgrade head` - Apply all migrations to the local database
  - `alembic downgrade -1` - Revert the last migration. Important to do before deleting a migration
    if you want to regenerate it.
