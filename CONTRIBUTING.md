# Contributing to Napoletano-Web

## Local Setup

    docker-compose build
    docker-compose up

### Database migrations

    docker-compose run web poetry run alembic revision --autogenerate -m "init"
    docker-compose run web poetry run alembic upgrade head

## Tests

    poetry run pytest