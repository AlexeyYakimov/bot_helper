from flask import Blueprint, request

from korona_service.korona_api import get_rate_for

korona_api_routes = Blueprint('korona_api', __name__, url_prefix='/v1/exchange')


@korona_api_routes.get('/korona-rates')
def corona_course():
    try:
        # TODO add API token
        if request.headers['Authorization'] == "":
            query = request.args
            amount = query.get("amount")

            return get_rate_for(int(amount)), 200
        else:
            return {'error': "Provide correct API token"}, 401
    except:
        return {'error': "Provide correct API token"}, 401