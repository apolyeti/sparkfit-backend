import boto3
import os
from tensorflow.keras.models import load_model
from flaskr.classes import SparkFitImage
from flaskr.classes import SparkFitUser
from flaskr.dynamo_handler import get_user

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
REGION = os.getenv('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)


s3 = session.client('s3')

def download_model():
    local_file_path = 'flaskr/aws/downloads/models/classify_clothes.keras'
    bucket_name = 'sparkfit'
    object_key = 'models/classify_clothes.keras'
    if not os.path.exists(local_file_path):
        print('\033[94m' + 'Model not found. Downloading from AWS S3...' + '\033[0m')
        try:
            s3.download_file(bucket_name, object_key, local_file_path)
            print('\033[92m' + 'Model downloaded successfully!' + '\033[0m')
        except Exception as e:
            print('\033[91m' + 'Error downloading model from S3: ' + str(e) + '\033[0m')
    else:
        print('\033[93m' + 'Model already found in downloads directory' + '\033[0m')

    return load_model(local_file_path)

model = download_model()

class_path = 'flaskr/utils/labels.txt'

with open(class_path, 'r') as f:
    class_names = f.read().splitlines()


def fetch_user_images(email):
    user = get_user(email)
    subdir_name = email.split('@')[0]
    object_key = f'images/{subdir_name}/'
    bucket_name = 'sparkfit'

    # return all file data in the user's directory
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=object_key)

    image_files = []

    for obj in response['Contents']:
        file_name = obj['Key']
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_data = response['Body'].read()

        image_files.append({
            'file_name': file_name,
            'data': file_data
        })

    return image_files

def upload_image(email, file_name, file_data):
    subdir_name = email.split('@')[0]
    object_key = f'images/{subdir_name}/{file_name}.jpg'
    bucket_name = 'sparkfit'

    response = s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_data)

    return response
