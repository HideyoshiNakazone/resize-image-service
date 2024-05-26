from storage_service.config.config_server import get_config_server
from storage_service.depends.depend_queue import dependency_queue_worker

import uvicorn

import argparse


def main(is_queue=False, is_dev=False):
    if is_queue:
        dependency_queue_worker().work(with_scheduler=True)
    else:
        config = {
            **get_config_server(),
            "reload": is_dev,
        }

        uvicorn.run("storage_service.__init__:app", **config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Storage Service")
    parser.add_argument(
        "-q",
        "--queue",
        dest="queue",
        default=False,
        action="store_true",
        help="Runs the worker to process the queue",
    )
    parser.add_argument(
        "-d",
        "--dev",
        dest="dev_mode",
        default=False,
        action="store_true",
        help="Run the server in development mode.",
    )

    args = parser.parse_args()

    main(args.queue, args.dev_mode)
