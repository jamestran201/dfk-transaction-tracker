#!/bin/bash

export DOCKER_BUILDKIT=1

# Dump requirements.txt to docker_build/ using Poetry
poetry export --format requirements.txt --output docker_build/requirements.txt --without-hashes

# Build Docker image for Celery
docker build --tag dfk-transaction-tracker-celery-worker:v0.1.0 --target celery_build .

# Build Docker image for Django app
docker build --tag dfk-transaction-tracker-app:v0.1.0 --target app_build .
