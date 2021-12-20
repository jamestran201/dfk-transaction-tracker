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

## Managing a local database

To create a database locally:
```bash
docker-compose up -d
```

To stop the local database:
```bash
docker-compose stop
```

To destroy the local database:
```bash
docker-compose down --volumes
```

## Running database migrations locally

To apply new database migrations:
```bash
make migrate-up
```
