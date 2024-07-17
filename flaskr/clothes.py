from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS
import requests
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import os
import io
import boto3

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

# Check if the model is already in the cache
if not os.path.exists(local_file_path):
    print('\033[94m' + 'Model not found. Downloading from AWS S3...' + '\033[0m')
    try:
        s3.download_file(bucket_name, object_key, local_file_path)
        print('\033[92m' + 'Model downloaded successfully!' + '\033[0m')
    except Exception as e:
        print('\033[91m' + 'Error downloading model from S3: ' + str(e) + '\033[0m')
else:
    print('\033[93m' + 'Model already found in downloads directory' + '\033[0m')

model = load_model(local_file_path)
print(model.summary())

class_path = 'flaskr/utils/labels.txt'

with open(class_path, 'r') as f:
    class_names = f.read().splitlines()

print('\033[1;92m' + 'Model and class names loaded successfully!' + '\033[0m')

bp = Blueprint('clothes', __name__, url_prefix='/clothes')
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

@bp.route('/classify', methods=['POST'])
def classify():
    """
    /clothes/classify
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
