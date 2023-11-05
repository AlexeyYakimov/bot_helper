from flask import Blueprint, jsonify, request

from in_memory_db.token_storage import get_token, Token
from weather_service.marine_api import get_current_weather, get_data

weather_api_routes = Blueprint('weather_api', __name__, url_prefix='/v1/weather')


@weather_api_routes.get('/current-hour')
def get_weather():
    try:
        if request.headers['Authorization'] == get_token(Token.API):
            return jsonify(get_current_weather()), 200
        else:
            return {'error': "Provide correct API token"}, 401
    except:
        return {'error': "Some thing went wrong"}, 500


@weather_api_routes.get('/all-day')
def get_weather_all_day():
    try:
        if request.headers['Authorization'] == get_token(Token.API):
            return jsonify(get_data()), 200
        else:
            return {'error': "Provide correct API token"}, 401
    except:
        return {'error': "Some thing went wrong"}, 500
