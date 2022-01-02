#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate

gunicorn dfk_transaction_tracker.wsgi --bind 0.0.0.0:8000
