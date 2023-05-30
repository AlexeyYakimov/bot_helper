from flask import Blueprint, request

from db.queues import get_last_korona_data
from in_memory_db.token_storage import Token, get_token
from korona_service.utils import calculate_amount

korona_api_routes = Blueprint('korona_api', __name__, url_prefix='/v1/exchange')


@korona_api_routes.get('/korona-rates')
def corona_course():
    try:
        if request.headers['Authorization'] == get_token(Token.API):
            query = request.args
            amount = query.get("amount", 1)
            data = calculate_amount(get_last_korona_data(), amount)

            open_json = "{"
            close_json = "}"
            response = f"""{open_json}
                        "timestamp": {data.timestamp},
                        "rate": {data.rate},
                        "sending_amount": {data.sending_amount},
                        "sending_currency": {data.sending_currency.name},
                        "receiving_amount": {data.receiving_amount},
                        "receiving_currency": {data.receiving_currency.name},
                        "commission": {data.commission}
                        {close_json}"""
            return response, 200
        else:
            return {'error': "Provide correct API token"}, 401
    except:
        return {'error': "Provide correct API token"}, 401
