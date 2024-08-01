import requests
from flask import Blueprint, request
from flask_cors import CORS

bp = Blueprint("getWeather", __name__)
CORS(bp, resources={r"/*": {"origins": "http://localhost:3000"}})


@bp.route("/getWeather", methods=["POST", "GET"])
def getWeather():
    """
    Get the weather at a given latitude and longitude.

    Parameters:
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
        API_KEY (str): The API key for the weather API.

    Returns:
        dict: The weather data at the given location.
    """
    if request.method == "POST":
        data = request.get_json()
        lat = data["lat"]
        lon = data["lon"]
        API_KEY = data["API_KEY"]

        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"

        response = requests.get(url)

        return response.json()

    if request.method == "GET":
        return "GET request for /getWeather/"
