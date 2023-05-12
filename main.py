import os

import aqi_service.handlers
import korona_service
import tg_bot
import weather_service
from korona_service.api import korona_api_routes
from server.api_server import flask_app
from tg_bot.api import bot_api_routes
from weather_service.api import weather_api_routes

if __name__ == '__main__':
    aqi_service.register_handlers()
    korona_service.register_handlers()
    weather_service.register_handlers()
    tg_bot.register_handlers()

    tg_bot.set_webhook()

    flask_app.register_blueprint(bot_api_routes)
    flask_app.register_blueprint(korona_api_routes)
    flask_app.register_blueprint(weather_api_routes)

    flask_app.run(host='0.0.0.0', port=os.environ.get("PORT", 8081))
