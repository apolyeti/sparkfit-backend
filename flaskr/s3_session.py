import boto3
import os
from tensorflow.keras.models import load_model

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
REGION = os.getenv('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)


local_file_path = 'flaskr/aws/downloads/models/classify_clothes.keras'
bucket_name = 'sparkfit'
object_key = 'models/classify_clothes.keras'

s3 = session.client('s3')

def download_model():
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

