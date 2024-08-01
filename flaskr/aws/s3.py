"""
This module contains functions for interacting with AWS S3 Bucket, as well as CloudFront CDN for image storage and retrieval.

Functions:
    download_classification_model: Downloads the classification model from S3.
    fetch_user_images: Fetches all images for a user from S3.
    upload_image: Uploads an image to S3.
    clear_user_directory: Clears all images for a user from S3.
"""
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import load_model, Model

from flaskr.aws.config import get_aws_session

session = get_aws_session()

s3 = session.client("s3")


def download_classification_model() -> Model:
    """
    Downloads the classification model from S3.

    Returns:
        keras.models.Model: The classification model.
    """

    local_file_path = os.path.join('flaskr', 'aws', 'downloads', 'models', 'classify_clothes.keras')
    
    bucket_name = "sparkfit"
    object_key = "models/classify_clothes.keras"
    # Download the model from S3 if it doesn't exist locally
    if not os.path.exists(local_file_path):
        print("\033[94m" + "Model not found. Downloading from AWS S3..." + "\033[0m")
        try:
            s3.download_file(bucket_name, object_key, local_file_path)
            print("\033[92m" + "Model downloaded successfully!" + "\033[0m")
        except Exception as e:
            print("\033[91m" + "Error downloading model from S3: " + str(e) + "\033[0m")
    else:
        print("\033[93m" + "Model already found in downloads directory" + "\033[0m")

    return load_model(local_file_path)


def fetch_user_images(email) -> list:
    """
    Fetches all images for a user from S3.

    Parameters:
        email (str): The user's email.

    Returns:
        list: A list of dictionaries containing the file name and data for each image.
    """
    subdir_name = email.split("@")[0]
    object_key = f"images/{subdir_name}/"
    bucket_name = "sparkfit"

    # return all file data in the user's directory
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=object_key)

    image_files = []

    for obj in response["Contents"]:
        file_name = obj["Key"]
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_data = response["Body"].read()

        image_files.append({"file_name": file_name, "data": file_data})

    return image_files



def upload_image(email, file_name, file_data) -> dict:
    """
    Uploads an image to S3.

    Parameters:
        email (str): The user's email.
        file_name (str): The name of the file.
        file_data (bytes): The image data.

    Returns:
        dict: The response from S3.
    """
    subdir_name = email.split("@")[0]
    object_key = f"images/{subdir_name}/{file_name}.jpg"
    bucket_name = "sparkfit"

    response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_data)

    return response


def clear_user_directory(email) -> dict:
    """
    Clears all images for a user from S3.

    Parameters:
        email (str): The user's email.

    Returns:
        dict: The response from S3.
    """
    subdir_name = email.split("@")[0]
    object_key = f"images/{subdir_name}/"
    bucket_name = "sparkfit"

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=object_key)

    for obj in response["Contents"]:
        file_name = obj["Key"]
        response = s3.delete_object(Bucket=bucket_name, Key=file_name)

    return response
