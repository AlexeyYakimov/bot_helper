import requests
import telebot
from flask import Flask, request
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import aqi_service.handlers
import korona_service
import marine
import tg_bot
import utils
from token_storage import get_bot_token, get_ngrok_token, get_alert_token

button_puk = 'Puk'
button_weather = 'Weather'
button_another_amount = 'Enter custom amount'
button_aqi = "AQI Batumi"

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton(button_puk), KeyboardButton(button_weather))
markup.add(KeyboardButton(button_another_amount), KeyboardButton(button_aqi))

aqi_description_inline_btn = types.InlineKeyboardButton(text='Aqi description',
                                                        callback_data="aqi_description")
inline_keyboard = types.InlineKeyboardMarkup()
inline_keyboard.add(aqi_description_inline_btn)

app = Flask(__name__)
# tg_bot = telebot.TeleBot(token=get_bot_token())

in_memory_cash = {}


def get_webhook_url(ngrok_t, bot_t) -> str:
    try:
        response = requests.get(url="https://api.ngrok.com/endpoints",
                                headers={'Authorization': f"Bearer {ngrok_t}",
                                         'Ngrok-Version': "2"})
        url = response.json()["endpoints"][0]["public_url"]
        return url + "/" + bot_t
    except:
        send_message(utils.my_id, "ngrok down")


@app.route('/' + get_bot_token(), methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    tg_bot.bot.bot.process_new_updates([update])
    return 'ok', 200


@app.route('/alert', methods=['POST'])
def send_alert_to():
    try:
        if request.headers['Authorization'] == get_alert_token():
            json_data = request.get_json()
            id = json_data.get('id', None)
            msg = json_data.get('msg')

            if id is not None:
                send_message(id, msg)
            else:
                send_message(utils.do_id, msg)
                send_message(utils.my_id, msg)

            return {'success': "Alert successfully send"}, 200
        else:
            return {'error': "Sorry wrong token"}, 401
    except:
        return {'error': "Sorry, server temporary down:("}, 500


aqi_service.register_handlers()
korona_service.register_handlers()


# @tg_bot.bot.bot.message_handler(commands=['start'])
# def start_handler(message):
#     send_message(message.chat.id, "Hi", keyboard=markup)
#

def start_handler(tbot, message):
    tbot.send_message(chat_id=message.chat.id, text="Hi registered", reply_markup=markup)


@tg_bot.bot.bot.message_handler(func=lambda message: message.text == button_weather, content_types=['text'])
def weather_handler(message):
    data = marine.get_data_message()
    send_message(message.chat.id, data, keyboard=markup)
    tg_bot.send_log_message(message, f"use {message.text}")


# @tg_bot.bot.bot.message_handler(func=lambda message: message.text.isdigit() and message.chat.id in in_memory_cash,
#                                 content_types=['text'])
# def amount_handler(message):
#     result = get_custom_amount(int(message.text))
#
#     if 'Exchange Rate' in result:
#         in_memory_cache.remove_key(message.chat.id)
#
#     send_message(message.chat.id, get_custom_amount(int(message.text)), keyboard=markup)
#
#     tg_bot.send_log_message(message, f"use Custom amount with {message.text}")

@tg_bot.bot.bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        send_message(message.chat.id, "Stop writing to me, i don't understand it:)\n"
                                      "Just push on the buttons under text message field.", markup)
    except:
        tg_bot.send_log_message(message, f"cant use {message.text}")
        send_message(message.chat.id, "something went wrong!")


def send_message(chat_id, data, keyboard=None):
    try:
        tg_bot.bot.bot.send_message(chat_id=chat_id, text=data, reply_markup=keyboard, parse_mode='HTML')

    except:
        try:
            tg_bot.bot.bot.send_message(chat_id=utils.my_id, text=f"Cant send message for {chat_id} with data {data}")
        except:
            print(f"Cant send message for {chat_id} with data {data}")


if __name__ == '__main__':
    bot_token = get_bot_token()
    ngrok_token = get_ngrok_token()

    ngrok_url = get_webhook_url(ngrok_t=ngrok_token, bot_t=bot_token)
    tg_bot.bot.bot.remove_webhook()
    # tg_bot.set_webhook(url=ngrok_url)
    tg_bot.bot.bot.infinity_polling()

    send_message(utils.my_id, f"Bot started {ngrok_url} \n\n Alert: {get_alert_token()}")
    # app.run(host='0.0.0.0', port=os.environ.get("PORT", 8081))
