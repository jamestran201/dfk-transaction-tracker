#!/bin/bash

export DOCKER_BUILDKIT=1

ACCOUNT_NAME="$1"
BUILD_TAG="$2"

# Dump requirements.txt to docker_build/ using Poetry
poetry export --format requirements.txt --output docker_build/requirements.txt --without-hashes

# Build Docker image for Celery
docker build --tag "$ACCOUNT_NAME/dfk-transaction-tracker-celery-worker:$BUILD_TAG" --target celery_build .

# Build Docker image for Django app
docker build --tag "$ACCOUNT_NAME/dfk-transaction-tracker-app:$BUILD_TAG" --target app_build .
