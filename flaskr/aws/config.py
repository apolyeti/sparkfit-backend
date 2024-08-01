"""
This module contains the configuration for the AWS session using the boto3 AWS SDK.
To use this module, set the following environment variables:
    - AWS_ACCESS_KEY_ID: The AWS access key ID.
    - AWS_SECRET_KEY_ID: The AWS secret access key.
    - AWS_REGION: The AWS region name.
For more information on AWS sessions, see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html

Functions:
    get_aws_session: Get an AWS session using the environment variables.

"""

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
