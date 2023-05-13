import telebot
from telebot import TeleBot

from in_memory_db.in_memory_data import my_id
from in_memory_db.token_storage import Token, get_token

bot: TeleBot = telebot.TeleBot(token=get_token(Token.TELEGRAM))


def send_message(chat_id, data, user_name, keyboard=None):
    try:
        bot.send_message(chat_id=chat_id, text=data, reply_markup=keyboard, parse_mode='HTML')
    except:
        try:
            bot.send_message(chat_id=my_id, text=f"Cant send message for {chat_id}/{user_name} with data {data}")
        except:
            print(f"Cant send message for {chat_id}/{user_name} with data {data}")


def send_log_message(chat_id, user_name, info: str):
    bot.send_message(my_id, f"User {chat_id}/{user_name} use {info}")
