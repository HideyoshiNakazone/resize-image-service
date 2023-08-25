#!/bin/sh


rq worker --with-scheduler

exec "$@"