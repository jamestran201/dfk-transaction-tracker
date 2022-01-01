#!/bin/bash

ACCOUNT_NAME="$1"
BUILD_TAG="$2"

docker push "$ACCOUNT_NAME/dfk-transaction-tracker-celery-worker:$BUILD_TAG"

docker push "$ACCOUNT_NAME/dfk-transaction-tracker-app:$BUILD_TAG"
