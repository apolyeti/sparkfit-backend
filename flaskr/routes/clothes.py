import base64
import uuid

import numpy as np
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from PIL import Image

from flaskr.aws import dynamo as db
from flaskr.aws.s3 import (
    download_classification_model,
    fetch_user_images,
    upload_image,
)
from flaskr.utils.classes import SparkFitImage

bp = Blueprint("clothes", __name__, url_prefix="/clothes")
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

model = download_classification_model()

print("\033[1;92m" + "Model loaded successfully!" + "\033[0m")


@bp.route("/classify", methods=["POST"])
def classify():
    """Will receive a list of files"""
    if "files" not in request.files:
        return jsonify({"error": "No files found in request"}), 400

    class_path = "flaskr/utils/labels.txt"

    with open(class_path, "r") as f:
        class_names = f.read().splitlines()

    files = request.files.getlist("files")

    results = []

    for file in files:
        file_contents = file.read()

        img = Image.open(file).convert("L")
        img = Image.eval(img, lambda x: 255 - x)
        img = img.resize((28, 28))
        img_array = np.array(img) / 255.0

        img_array = np.expand_dims(img_array, axis=(0, -1))

        predictions = model.predict(img_array)
        # get top 5 predictions
        top_5 = np.argsort(predictions[0])[-5:][::-1]

        encoded_image = base64.b64encode(file_contents).decode("utf-8")

        new_sparkfit_image = SparkFitImage(
            photo_id=str(uuid.uuid4()),
            predicted_classes=[class_names[i] for i in top_5],
            category=class_names[top_5[0]],
            file_name=file.filename,
            data=encoded_image,
            fabric=None,
            color=None,
            fit=None,
        )

        results.append(new_sparkfit_image)

    response = {"results": [result.__dict__ for result in results]}

    return jsonify(response), 200


@bp.route("/add", methods=["POST"])
def add_clothes():
    """Add a user's clothes to the database"""
    data = request.get_json()
    email = data["email"]
    clothes = data["clothes"]

    # translate to SparkFitImage objects
    clothes = [SparkFitImage(**cloth) for cloth in clothes]

    db.add_clothes(email, clothes)

    for cloth in clothes:
        image_data = base64.b64decode(cloth.data)
        upload_image(email, file_name=cloth.photo_id, file_data=image_data)

    response = {"message": "Clothes added to DynamoDB and S3 successfully"}

    return jsonify(response), 200


@bp.route("/get", methods=["POST"])
def get_clothes():
    """Get a user's clothes from the database"""

    # get clothes from database, then get the images from S3
    data = request.get_json()
    email = data["email"]

    clothes = db.get_clothes(email)

    if not clothes:
        return jsonify({"clothes": []}), 200

    # now get images from s3
    file_data = fetch_user_images(email)

    for file in file_data:
        # photo id is the file name before the .jpg
        photo_id = file["file_name"].split("/")[-1].split(".")[0]
        for cloth in clothes:
            if cloth["photo_id"] == photo_id:
                # give data url in base64
                cloth["data_url"] = "data:image/jpeg;base64," + base64.b64encode(
                    file["data"]
                ).decode("utf-8")
                break

    response = {"clothes": clothes}

    return jsonify(response), 200
