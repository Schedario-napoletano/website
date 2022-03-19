# Contributing to Napoletano-Web

## Local Setup

    docker-compose build
    docker-compose up

### Database migrations

    docker-compose run web poetry run alembic revision --autogenerate -m "init"
    docker-compose run web poetry run alembic upgrade head

### PgAdmin

    docker-compose up pgadmin

Then go to <http://localhost:5050/>. The credentials are `pgadmin4@pgadmin.org` / `admin`. Connect to the server using
the address `db`, username `postgres` and password `postgres`.

### Import definitions

    cat definitions.json | docker-compose run web poetry run python import_definitions.py

## Tests

    poetry run pytest