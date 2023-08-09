from resize_image_service.config.config_redis import get_config_redis

from redis import Redis
from rq import Queue


def dependency_queue():
    return Queue(connection=Redis(**get_config_redis()))
