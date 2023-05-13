import telebot
from flask import Blueprint, request

from tg_bot import bot
from in_memory_db.in_memory_data import do_id, my_id
from in_memory_db.token_storage import Token, get_token

bot_api_routes = Blueprint('telegram_api', __name__)


@bot_api_routes.post('/' + get_token(Token.TELEGRAM))
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.bot.process_new_updates([update])
    return 'ok', 200


@bot_api_routes.post('/alert')
def send_alert_to():
    try:
        if request.headers['Authorization'] == get_token(Token.ALERT):
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
        return {'error': "Provide correct API token"}, 401
