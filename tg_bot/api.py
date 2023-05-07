import telebot
from flask import Blueprint, request

from tg_bot import bot
from utils.global_utils import do_id, my_id
from utils.token_storage import get_bot_token, get_alert_token

bot_api_routes = Blueprint('simple_page', __name__)


@bot_api_routes.post('/' + get_bot_token())
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.bot.process_new_updates([update])
    return 'ok', 200


@bot_api_routes.post('/alert')
def send_alert_to():
    try:
        if request.headers['Authorization'] == get_alert_token():
            json_data = request.get_json()
            chat_id = json_data.get('id', None)
            msg = json_data.get('msg')

            if chat_id is not None:
                bot.send_message(chat_id, msg)
            else:
                bot.send_message(do_id, msg)
                bot.send_message(my_id, msg)

            return {'success': "Alert successfully send"}, 200
        else:
            return {'error': "Sorry wrong token"}, 401
    except:
        return {'error': "Sorry, server temporary down:("}, 500
