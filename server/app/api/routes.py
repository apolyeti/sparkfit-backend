from flask import Blueprint, jsonify
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import boto3
import os

# following this docstring format:
# https://stackoverflow.com/a/43912874/18797962
# https://swagger.io/docs/specification/describing-parameters/

# retrieve access key and secret key from environment variables
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_KEY_ID')
REGION = os.getenv('AWS_REGION')

api = Blueprint('api', __name__)

# Load the trained model
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

bucket_name = 'sparkfit'
object_key = 'models/classify_clothes.keras'
local_file_path = 'aws/downloads/models/classify_clothes.keras'

s3 = session.client('s3')

s3.download_file(bucket_name, object_key, local_file_path)




@api.route('/classifyClothing', methods=['POST'])
def classify_clothing():
    """
    /api/classifyClothing
    ---
    tags:
      - Clothing Classification
    description: Classify clothing using a trained model
    parameters:
        -   name: name
            in: query
            type: string
            required: true
            description: The name of the image file
        -   name: image
            in: query
            type: file
            required: true
            description: The image file to classify
    responses:
        200:
            description: Clothing classification successful
        400:
            description: Bad request
        500:
            description: Internal server error
    """
    print('Classifying clothing...')
    return jsonify({'message': 'Classifying clothing...'})




@api.route('/classifyClothing', methods=['GET'])
def classify_clothing_get():
    return jsonify({'message': 'GET request received'})

@api.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the SparkFit API!'})