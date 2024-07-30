import base64
import uuid
import threading

import numpy as np
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from PIL import Image
import json

from flaskr.aws import dynamo as db
from flaskr.aws.s3 import (
    download_classification_model,
    fetch_user_images,
    upload_image,
)
from flaskr.utils.classes import SparkFitImage, DynamoImage
from flaskr.utils.sparkfit_llm import SparkfitLLM

llm = SparkfitLLM()

def load_model():
    llm.load_model()
    print("\033[1;92m" + "Sparkfit-LLM loaded successfully!" + "\033[0m")

threading.Thread(target=load_model).start()

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

@bp.route("/outfit", methods=["POST"])
def outfit():
    """Will receive a list of
    SparkfitImage objects
    """

    print("Outfit request received")

    # send the photo_id, category, fabric, color, fit to the model

    data = request.get_json()
    email = data["email"]
    clothes = data["clothes"]
    temperature = data["temperature"]
    condition = data["condition"]

    # translate to DynamoImage objects
    clothes = [DynamoImage(**cloth) for cloth in clothes]



    # prompt = "\nYour Prompt:\n"

    prompt = ""

    for cloth in clothes:
        prompt += f"{cloth.photo_id}, {cloth.color}, {cloth.fabric}, {cloth.fit}, {cloth.category}; "

    prompt += f"Weather: {temperature}, {condition}"

    prompt += "\nYour Response:\n"

    # check if the model is loaded
    while not llm.is_loaded:
        pass



    generate = llm.generate_text(prompt)
    
    # the string is in json format, so we need to convert it to a dictionary and return that as the response
    response_dict = json.loads(generate)

    print(len(response_dict["choices"]))

    image_files = fetch_user_images(email)

    response = {"choices": []}

    outfits = {
        "outfit": [],
        "temperature": temperature,
        "condition": condition
    }

    for choice in response_dict["choices"]:
        outfit = {
            "reasoning": choice.get("reasoning", ""),
            "clothes": []
        }
        for clothing_item in choice["outfit"]:
            item = {
                "photo_id": clothing_item.get("photo_id", ""),
                "fabric": clothing_item.get("fabric", ""),
                "color": clothing_item.get("color", ""),
                "fit": clothing_item.get("fit", ""),
                "category": clothing_item.get("category", ""),
            }
            for file in image_files:
                photo_id = file["file_name"].split("/")[-1].split(".")[0]
                if clothing_item["photo_id"] == photo_id:
                    item["data_url"] = "data:image/jpeg;base64," + base64.b64encode(file["data"]).decode("utf-8")
                    break
            outfit["clothes"].append(item)
        outfits["outfit"].append(outfit)

    # Create a copy of outfits without the data_url for DynamoDB storage
    outfits_without_data_url = {
        "outfit": [],
        "temperature": temperature,
        "condition": condition
    }
    for outfit in outfits["outfit"]:
        outfit_copy = {
            "reasoning": outfit["reasoning"],
            "clothes": []
        }
        for clothing_item in outfit["clothes"]:
            item_copy = {k: v for k, v in clothing_item.items() if k != "data_url"}
            outfit_copy["clothes"].append(item_copy)
        outfits_without_data_url["outfit"].append(outfit_copy)

    db.add_outfit(email, [outfits_without_data_url])
    
    response["choices"] = response_dict["choices"]

    return jsonify(response), 200
    


