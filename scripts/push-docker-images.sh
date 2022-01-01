#!/bin/bash

BUILD_TAG="$1"

docker push "jamestran/dfk-transaction-tracker-celery-worker:$BUILD_TAG"

docker push "jamestran/dfk-transaction-tracker-app:$BUILD_TAG"
