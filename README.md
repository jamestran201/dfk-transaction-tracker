# dfk-transaction-tracker

## Pre-requisites

- Python 3.8
- [Poetry](https://python-poetry.org/docs/#installation)

## Set up the Python project

- Install dependencies: `poetry install`
- Activate virtualenv: `. .venv/bin/activate`

## Adding a new Python dependency

- Run `poetry add package-name`. Replace `package-name` with the dependency name, and pin the dependency version when possible
- Check in the `poetry.toml` and `Poetry.lock` files to Git
