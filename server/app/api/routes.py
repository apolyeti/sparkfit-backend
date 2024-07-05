from flask import Blueprint, jsonify, request
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import boto3
import os
import io
from PIL import Image

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

# check if we already have downloaded the model
if not os.path.exists(local_file_path):
    print('\033[94m' + 'Model not found. Downloading from S3...' + '\033[0m')
    try:
        s3.download_file(bucket_name, object_key, local_file_path)
        print('\033[92m' + 'Model downloaded successfully!' + '\033[0m')
    except Exception as e:
        print('\033[91m' + 'Error downloading model: ' + str(e) + '\033[0m')
else:
    print('\033[93m' + 'Model already found in downloads directory' + '\033[0m')

model = load_model(local_file_path)
print(model.input_shape)

# Load the class names
class_path = 'utils/labels.txt'

with open(class_path, 'r') as f:
    class_names = f.read().splitlines()

print('\033[1;92m' + 'Model and class names loaded successfully!' + '\033[0m')




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

    # get json data
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # make greyscale and invert colors
        img = Image.open(file).convert('L')
        img = Image.eval(img, lambda x: 255-x)
        img = img.resize((28, 28))
        img_array = np.array(img) / 255.0


        img_array = np.expand_dims(img_array, axis=(0, -1))

        # download image as it is and save it
        # img.save('aws/downloads/' + file.filename)

        predictions = model.predict(img_array)
        # get top 3 predictions
        top3 = np.argsort(predictions[0])[-3:][::-1]

        top_3_classes = [class_names[i] for i in top3]


        response = {
            'predictions': top_3_classes,
            'file_name': file.filename
        }

        return jsonify(response), 200





@api.route('/classifyClothing', methods=['GET'])
def classify_clothing_get():
    return jsonify({'message': 'GET request received'})

@api.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the SparkFit API!'})