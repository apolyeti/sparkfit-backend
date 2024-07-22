from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS # type: ignore
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np
from PIL import Image
import uuid

import os
import io
import boto3
import requests
import base64

from flaskr.classes import SparkFitImage
from flaskr.s3_session import model, class_names, upload_image
import flaskr.dynamo_handler as db

print('\033[1;92m' + 'Model and class names loaded successfully!' + '\033[0m')
# print(model.summary())


bp = Blueprint('clothes', __name__, url_prefix='/clothes')
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

@bp.route('/classify', methods=['POST'])
def classify():
    """Will receive a list of files """
    if 'files' not in request.files:
        return jsonify({'error': 'No files found in request'}), 400


    files = request.files.getlist('files')
    
    results = []
    
    for file in files:
        file_contents = file.read()

        img = Image.open(file).convert('L')
        img = Image.eval(img, lambda x: 255 - x)
        img = img.resize((28, 28))
        img_array = np.array(img) / 255.0

        img_array = np.expand_dims(img_array, axis=(0, -1))

        predictions = model.predict(img_array)
        # get top 5 predictions
        top_5 = np.argsort(predictions[0])[-5:][::-1]

        encoded_image = base64.b64encode(file_contents).decode('utf-8')

        new_sparkfit_image = SparkFitImage(
            photo_id=str(uuid.uuid4()),
            predicted_classes=[class_names[i] for i in top_5],
            category=class_names[top_5[0]],
            file_name=file.filename,
            data=encoded_image,
            fabric=None,
            color=None,
            fit=None
        )

        results.append(new_sparkfit_image)



    response = {
        'results': [result.__dict__ for result in results]
    }

    return jsonify(response), 200

@bp.route('/add', methods=['POST'])
def add_clothes():
    """Add a user's clothes to the database"""
    data = request.get_json()
    email = data['email']
    clothes = data['clothes']

    # translate to SparkFitImage objects
    clothes = [SparkFitImage(**cloth) for cloth in clothes]

    db.add_clothes(email, clothes)

    for cloth in clothes:
        image_data = base64.b64decode(cloth.data)
        upload_image(email, file_name=cloth.photo_id, file_data=image_data)


    response = {
        'message': 'Clothes added to DynamoDB and S3 successfully'
    }

    return jsonify(response), 200