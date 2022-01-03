#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


celery -A dfk_transaction_tracker worker -l INFO --concurrency 4 --without-heartbeat --without-gossip --without-mingle -Ofair
