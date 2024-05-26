from storage_service.config.config_redis import get_config_redis

from redis import Redis
from rq import Queue, Worker

from functools import cache


@cache
def dependency_queue() -> Queue:
    return Queue(name="default", connection=Redis(**get_config_redis()))


@cache
def dependency_queue_worker() -> Worker:
    return Worker(["default"], connection=Redis(**get_config_redis()))
