from flask import Flask, Blueprint, request

from in_memory_db.token_storage import get_token, Token

flask_app = Flask(__name__)

server_api_routes = Blueprint('server_api', __name__, url_prefix='/tech')

# curl -H "Authorization: $API_TOKEN" https://$PROXY_DOMAIN.loca.lt/tech/ping


@server_api_routes.get("/ping")
def ping_server():
    if request.headers['Authorization'] == get_token(Token.API):
        return {"status": "OK"}, 200
    else:
        return {"status": "need token"}, 401


@flask_app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response

