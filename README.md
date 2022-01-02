# dfk-transaction-tracker

## Pre-requisites

- Python 3.8
- [Poetry](https://python-poetry.org/docs/#installation)
- Make
- [yarn](https://yarnpkg.com/getting-started/install)

## Set up the development environment

- Install dependencies: `make install`
- Activate virtualenv: `. .venv/bin/activate`
- Create a `.env` file to store environment variables for local development: `cp .env.example .env`
- In the `static/` directory, run `yarn install`

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

## Starting the Django server locally

```bash
make runserver
```

## Build and Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md)
