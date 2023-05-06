import os

from flask import Flask, request
import telebot
import requests
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import marine
import aqi_service.iquair_service
from korona_api import get_custom_amount
from token_storage import get_bot_token, get_ngrok_token, get_alert_token
import utils

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
bot = telebot.TeleBot(token=get_bot_token())

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
    bot.process_new_updates([update])
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


@bot.message_handler(commands=['start'])
def start_handler(message):
    send_message(message.chat.id, "Hi", keyboard=markup)


@bot.message_handler(func=lambda message: message.text == button_weather, content_types=['text'])
def weather_handler(message):
    data = marine.get_data_message()
    send_message(message.chat.id, data, keyboard=markup)
    utils.send_log_message(bot, message, f"use {message.text}")


@bot.message_handler(func=lambda message: message.text == button_puk, content_types=['text'])
def money_handler(message):
    send_message(message.chat.id, get_custom_amount(), keyboard=markup)
    utils.send_log_message(bot, message, f"use {message.text}")


@bot.message_handler(func=lambda message: message.text == button_another_amount, content_types=['text'])
def another_amount_handler(message):
    in_memory_cash[message.chat.id] = message.chat.username
    send_message(message.chat.id, "Enter amount in lari ₾:", keyboard=markup)
    utils.send_log_message(bot, message, f"use {message.text}")


@bot.message_handler(func=lambda message: message.text.isdigit() and message.chat.id in in_memory_cash,
                     content_types=['text'])
def amount_handler(message):
    result = get_custom_amount(int(message.text))

    if 'Exchange Rate' in result:
        utils.remove_key_safe(in_memory_cash, message.chat.id)

    send_message(message.chat.id, get_custom_amount(int(message.text)), keyboard=markup)

    utils.send_log_message(bot, message, f"use Custom amount with {message.text}")


@bot.message_handler(func=lambda message: message.text == button_aqi, content_types=['text'])
def aqi_message_handler(message):
    send_message(message.chat.id, aqi_service.iquair_service.get_data(), keyboard=inline_keyboard)
    utils.send_log_message(bot, message, f"use {message.text}")


@bot.callback_query_handler(func=lambda call: call.data == 'aqi_description')
def aqi_description_handler(call):
    send_message(call.from_user.id, aqi_service.iquair_service.get_description(), keyboard=markup)
    utils.send_log_message_call(bot, call, f"use {call.data}")


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        send_message(message.chat.id, "Stop writing to me, i don't understand it:)\n"
                                      "Just push on the buttons under text message field.", markup)
    except:
        utils.send_log_message(bot, message, f"cant use {message.text}")
        send_message(message.chat.id, "something went wrong!")


def send_message(chat_id, data, keyboard=None):
    try:
        bot.send_message(chat_id=chat_id, text=data, reply_markup=keyboard, parse_mode='HTML')

        utils.remove_key_safe(in_memory_cash, chat_id)
    except:
        bot.send_message(chat_id=utils.my_id, text=f"Cant send message for {chat_id} with data {data}")
    finally:
        print(f"Cant send message for {chat_id} with data {data}")


if __name__ == '__main__':
    bot_token = get_bot_token()
    ngrok_token = get_ngrok_token()

    ngrok_url = get_webhook_url(ngrok_t=ngrok_token, bot_t=bot_token)
    bot.remove_webhook()
    bot.set_webhook(url=ngrok_url)

    send_message(utils.my_id, f"Bot started {ngrok_url} \n\n Alert: {get_alert_token()}")
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 8081))
