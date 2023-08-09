from resize_image_service.config.config_server import get_config_server
from resize_image_service.controller import app

import uvicorn


def main():
    config = get_config_server()

    uvicorn.run(app, host=config["host"], port=config["port"])


if __name__ == "__main__":
    main()
