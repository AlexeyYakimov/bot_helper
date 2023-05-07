import telebot
from flask import request

from utils.global_utils import do_id, my_id
from server.api_server import flask_app
from utils.token_storage import get_bot_token, get_alert_token
import tg_bot as bot
from tg_bot.bot import bot as main_bot


@flask_app.post('/' + get_bot_token())
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    main_bot.process_new_updates([update])
    return 'ok', 200


@flask_app.post('/alert')
def send_alert_to():
    try:
        if request.headers['Authorization'] == get_alert_token():
            json_data = request.get_json()
            id = json_data.get('id', None)
            msg = json_data.get('msg')

            if id is not None:
                bot.send_message(id, msg)
            else:
                bot.send_message(do_id, msg)
                bot.send_message(my_id, msg)

            return {'success': "Alert successfully send"}, 200
        else:
            return {'error': "Sorry wrong token"}, 401
    except:
        return {'error': "Sorry, server temporary down:("}, 500

