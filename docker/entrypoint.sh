#!/bin/bash
set -eux

cd /app

run_app() {
    AUTOMIGRATE=${AUTOMIGRATE:-yes}
    NUM_WORKERS_DEFAULT=$((1 * $(nproc --all)))
    export NUM_WORKERS=${NUM_WORKERS:-$NUM_WORKERS_DEFAULT}

    if [ "$AUTOMIGRATE" != "skip" ]; then
        python ilmo/main.py migrate --noinput
    fi

    python ilmo/main.py collectstatic --noinput

    exec python -m gunicorn ilmo.wsgi \
        --name ilmo \
        --workers $NUM_WORKERS \
        --max-requests 1200 \
        --max-requests-jitter 50 \
        --log-level=info \
        --bind 0.0.0.0:8000
}

TARGET_UID="${ILMO_LOCAL_USER_ID:-0}"

# Get current UID
CURRENT_UID="$(id -u)"

# If LOCAL_USER_ID is set and user is not that already -> drop privileges
if [ -n "$TARGET_UID" ] && [ "$CURRENT_UID" != "$TARGET_UID" ]; then
    useradd -u "${TARGET_UID}" -o -m runuser 2>/dev/null || true
    chown -R runuser:runuser /app

    # Rerun the same entrypoint as runuser
    exec gosu runuser "$0"
fi

# If already running as runuser -> start app
run_app