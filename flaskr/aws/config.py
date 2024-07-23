import os
import boto3

def get_aws_session():
    _ACCESS_KEY  = os.getenv('AWS_ACCESS_KEY_ID')
    _SECRET_KEY  = os.getenv('AWS_SECRET_KEY_ID')
    _REGION      = os.getenv('AWS_REGION')

    return boto3.Session(
        aws_access_key_id=_ACCESS_KEY,
        aws_secret_access_key=_SECRET_KEY,
        region_name=_REGION
    )
