#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


celery -A dfk_transaction_tracker worker -l INFO --detach --concurrency 1

gunicorn dfk_transaction_tracker.wsgi --bind 0.0.0.0:8000
