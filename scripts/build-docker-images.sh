#!/bin/bash

export DOCKER_BUILDKIT=1

BUILD_TAG="$1"

# Dump requirements.txt to docker_build/ using Poetry
poetry export --format requirements.txt --output docker_build/requirements.txt --without-hashes

# Build Docker image for Celery
docker build --tag "jamestran/dfk-transaction-tracker-celery-worker:$BUILD_TAG" --target celery_build .

# Build Docker image for Django app
docker build --tag "jamestran/dfk-transaction-tracker-app:$BUILD_TAG" --target app_build .
