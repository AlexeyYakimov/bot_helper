import os

import aqi_service.handlers
import korona_service
import tg_bot
import weather_service
from server.api_server import flask_app

aqi_service.register_handlers()
korona_service.register_handlers()
weather_service.register_handlers()
tg_bot.register_handlers()

if __name__ == '__main__':
    tg_bot.set_webhook()

    flask_app.run(host='0.0.0.0', port=os.environ.get("PORT", 8081))
