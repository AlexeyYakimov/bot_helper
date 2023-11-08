import os

import aqi_service.handlers
import korona_service
import tg_bot
import weather_service
from db import init_db_tables
from korona_service.api import korona_api_routes
from schedule_runner import add_all_tasks, run_cron, clean_cron
from server.api_server import flask_app, server_api_routes
from tg_bot.api import bot_api_routes
from weather_service.api import weather_api_routes

if __name__ == '__main__':
    aqi_service.register_handlers()
    korona_service.register_handlers()
    weather_service.register_handlers()
    tg_bot.register_handlers()

    tg_bot.set_webhook()

    flask_app.register_blueprint(server_api_routes)
    flask_app.register_blueprint(bot_api_routes)
    flask_app.register_blueprint(korona_api_routes)
    flask_app.register_blueprint(weather_api_routes)

    init_db_tables()

    clean_cron()
    add_all_tasks()
    run_cron()

    flask_app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 8081))
