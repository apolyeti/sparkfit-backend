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

# Load the model in a background thread so that the route can be used immediately

# START THREAD
def load_model():
    llm.load_model()
    print("\033[1;92m" + "Sparkfit-LLM loaded successfully!" + "\033[0m")

threading.Thread(target=load_model).start()
# END THREAD

bp = Blueprint("clothes", __name__, url_prefix="/clothes")
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

model = download_classification_model()
print("\033[1;92m" + "Model loaded successfully!" + "\033[0m")


@bp.route("/classify", methods=["POST"])
def classify():
    """
    Classify an uploaded image.

    Parameters:
        files (list): A list of image files to classify.

    Returns:
        dict: The classification results.
    """
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
    """
    Add clothes to the database.

    Parameters:
        email (str): The user's email.
        clothes (list): A list of SparkFitImage objects representing the clothes.

    Returns:
        dict: A message indicating the success of the operation.
    """
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
    """
    Get clothes from the database.

    Parameters:
        email (str): The user's email.

    Returns:
        dict: A list of the user's clothes.
    """

    # get clothes from database, then get the images from S3
    data = request.get_json()
    email = data["email"]

    clothes = db.get_clothes(email)

    if not clothes:
        return jsonify({"clothes": []}), 200

    # now get images from s3
    file_data = fetch_user_images(email)

    email = email.split("@")[0]

    for file in file_data:
        # photo id is the file name before the .jpg
        photo_id = file["file_name"].split("/")[-1].split(".")[0]
        for cloth in clothes:
            if cloth["photo_id"] == photo_id:
                # give data url in base64
                cloth["data_url"] = "https://d1kqmt6gl9p8lg.cloudfront.net/images/" + email + "/" + photo_id + ".jpg"
                break

    response = {"clothes": clothes}

    return jsonify(response), 200

@bp.route("/delete", methods=["POST"])
def delete_clothes():
    """
    Delete clothes from the database.

    Parameters:
        email (str): The user's email.
        photo_id (str): The photo ID of the clothes to delete.

    Returns:
        dict: A message indicating the success of the operation.
    """

    data = request.get_json()
    email = data["email"]
    photo_id = data["photo_id"]

    db.delete_clothes(email, photo_id)

    response = {"message": "Clothes deleted from DynamoDB successfully"}

    return jsonify(response), 200

@bp.route("/update", methods=["POST"])
def update_clothes():
    """
    Update clothes in the database.

    Parameters:
        email (str): The user's email.
        updatedItem (dict): The updated clothing item.

    Returns:
        dict: A message indicating the success of the operation.
    """

    data = request.get_json()
    email = data["email"]
    cloth = data["updatedItem"]

    db.update_clothes(email, cloth)

    response = {"message": "Clothes updated in DynamoDB successfully"}

    return jsonify(response), 200


@bp.route("/outfit", methods=["POST"])
def outfit():
    """
    Generate an outfit based on the user's clothes and the weather.

    Parameters:
        email (str): The user's email.
        clothes (list): A list of DynamoImage objects representing the clothes.
        temperature (int): The temperature.
        condition (str): The weather condition.

    Returns:
        dict: The generated outfit.
    """
    data = request.get_json()
    email = data["email"]
    clothes = data["clothes"]
    temperature = data["temperature"]
    condition = data["condition"]

    # translate to DynamoImage objects
    clothes = [DynamoImage(**cloth) for cloth in clothes]

    prompt = ""

    for cloth in clothes:
        prompt += f"{cloth.photo_id}, {cloth.color}, {cloth.fabric}, {cloth.fit}, {cloth.category}; "

    prompt += f"Weather: {temperature}, {condition}"

    prompt += "\nYour Response:\n"

    # Stall until the model is loaded
    while not llm.is_loaded:
        pass

    generate = llm.generate_better_text(prompt)
    
    # Response is a JSON formatted string
    response = json.loads(generate)

    print("Sparkfit produced", len(response["choices"]), "outfit choices for", email)

    for choice in response["choices"]:
        for item in choice["outfit"]:
            item["data_url"] = "https://d1kqmt6gl9p8lg.cloudfront.net/images/" + email.split("@")[0] + "/" + item["photo_id"] + ".jpg"
    
    db.add_outfit(email, response["choices"])

    return jsonify(response), 200
    


