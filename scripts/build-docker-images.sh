#!/bin/bash

export DOCKER_BUILDKIT=1

# Dump requirements.txt to docker_build/ using Poetry
poetry export --format requirements.txt --output docker_build/requirements.txt --without-hashes

# Build Docker image for Celery
