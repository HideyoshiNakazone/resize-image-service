#!/bin/bash


if [[ $1 == "--queue" || $1 == "-q" ]]; then
    rq worker --with-scheduler
    exit 0
else
  python -m storage_service
fi

exec "$@"