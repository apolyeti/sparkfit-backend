from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS
import requests


bp = Blueprint('getWeather', __name__)
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})

@bp.route('/getWeather', methods=['POST', 'GET'])
def getWeather():
    """Get geolocation from request and return weather data"""
    if request.method == 'POST':
        data = request.get_json()
        lat = data['lat']
        lon = data['lon']
        API_KEY = data['API_KEY']

        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"

        response = requests.get(url)

        return response.json()

    if request.method == 'GET':
        return 'GET request for /getWeather/'