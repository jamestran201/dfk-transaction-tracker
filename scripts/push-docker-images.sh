#!/bin/bash

BUILD_TAG="$1"

docker push "us-central1-docker.pkg.dev/integral-nimbus-336917/dfk-transaction-tracker/dfk-transaction-tracker-celery-worker:$BUILD_TAG"

docker push "us-central1-docker.pkg.dev/integral-nimbus-336917/dfk-transaction-tracker/dfk-transaction-tracker-app:$BUILD_TAG"
