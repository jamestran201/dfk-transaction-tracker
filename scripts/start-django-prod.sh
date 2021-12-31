#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py migrate

# python manage.py compress
python manage.py collectstatic --noinput

gunicorn dfk_transaction_tracker.wsgi --bind 0.0.0.0:8000
