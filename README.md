# dfk-transaction-tracker

## Pre-requisites

- Python 3.8
- [Poetry](https://python-poetry.org/docs/#installation)
- Make

## Set up the Python project

- Install dependencies: `make install`
- Activate virtualenv: `. .venv/bin/activate`
- Create a `.env` file to store environment variables for local development: `cp .env.example .env`

## Adding a new Python dependency

- Run `poetry add package-name`. Replace `package-name` with the dependency name, and pin the dependency version when possible
- Check in the `poetry.toml` and `Poetry.lock` files to Git

## Managing local database and Redis instances

To create the instances locally:
```bash
docker-compose up -d
```

To stop all instances:
```bash
docker-compose stop
```

To destroy all instances:
```bash
docker-compose down --volumes
```

## Running database migrations locally

To apply new database migrations:
```bash
make migrate-up
```

## Starting a Celery worker locally

```bash
make start-celery
```
