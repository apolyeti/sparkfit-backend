from flask import Blueprint, jsonify

# following this docstring format:
# https://stackoverflow.com/a/43912874/18797962
# https://swagger.io/docs/specification/describing-parameters/

api = Blueprint('api', __name__)




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
    return jsonify({'message': 'Classifying clothing...'})