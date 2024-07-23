from flask import (
    Blueprint, request, jsonify
)
from flask_cors import CORS
import flaskr.aws.dynamo_handler as db
from flaskr.classes import SparkFitUser

bp = Blueprint('user', __name__, url_prefix='/user')
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

@bp.route('/add', methods=['POST'])
def add_user():
    """Add a user to the database"""
    data = request.get_json()
    
    email       = data['email']
    first_name  = data['first_name']
    last_name   = data['last_name']
    clothes     = data['clothes']

    new_user = SparkFitUser(first_name, last_name, email, clothes)

    db.add_user(new_user)
    # response will be either success of registering or just a message that the user already exists

    response = {
        'message': 'User signed into DynamoDB successfully'
    }

    return jsonify(response), 200

