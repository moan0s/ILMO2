#!/bin/bash

set -eux

cd /var/ilmo/src
export DATA_DIR=/var/ilmo/
source /var/ilmo/venv/bin/activate

AUTOMIGRATE=${AUTOMIGRATE:-yes}
NUM_WORKERS_DEFAULT=$((2 * $(nproc --all)))
export NUM_WORKERS=${NUM_WORKERS:-$NUM_WORKERS_DEFAULT}

if [ "$AUTOMIGRATE" != "skip" ]; then
  ilmo-manage migrate --noinput
fi

exec gunicorn ilmo.wsgi \
    --name ilmo \
    --workers $NUM_WORKERS \
    --max-requests 1200 \
    --max-requests-jitter 50 \
    --log-level=info \
    --bind 0.0.0.0:8345

