import telebot
from telebot import TeleBot

from utils.global_utils import my_id
from utils.token_storage import Token, get_token

bot: TeleBot = telebot.TeleBot(token=get_token(Token.TELEGRAM))


def send_message(chat_id, data, keyboard=None):
    try:
        bot.send_message(chat_id=chat_id, text=data, reply_markup=keyboard, parse_mode='HTML')
        send_log_message(chat_id, data)
    except:
        try:
            bot.send_message(chat_id=my_id, text=f"Cant send message for {chat_id} with data {data}")
        except:
            print(f"Cant send message for {chat_id} with data {data}")


def send_log_message(chat_id, info: str):
    bot.send_message(my_id, f"User {chat_id} use {info}")


def send_log_message_call(call, info: str):
    bot.send_message(my_id, f"User {call.from_user.id} {info}")
