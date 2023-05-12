from flask import Blueprint, jsonify, request

from utils.token_storage import get_token, Token
from weather_service.marine_api import get_current_weather

weather_api_routes = Blueprint('weather_api', __name__, url_prefix='/v1/weather')


@weather_api_routes.get('/')
def get_weather():
    try:
        if request.headers['Authorization'] == get_token(Token.API):
            return jsonify(get_current_weather()), 200
        else:
            return {'error': "Provide correct API token"}, 401
    except:
        return {'error': "Provide correct API token"}, 401
