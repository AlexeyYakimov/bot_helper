from flask import Flask

flask_app = Flask(__name__)


@flask_app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response
