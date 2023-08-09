from dotenv import load_dotenv

import os


def get_config_s3():
    load_dotenv()
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", None),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        "region_name": os.environ.get("AWS_REGION_NAME", None),
        "bucket_name": os.environ.get("AWS_BUCKET_NAME", None),
    }
