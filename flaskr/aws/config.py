import os

import boto3


def get_aws_session():
    """
    Get an AWS session using the environment variables.
    See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    """
    _ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    _SECRET_KEY = os.getenv("AWS_SECRET_KEY_ID")
    _REGION = os.getenv("AWS_REGION")

    return boto3.Session(
        aws_access_key_id=_ACCESS_KEY,
        aws_secret_access_key=_SECRET_KEY,
        region_name=_REGION,
    )
