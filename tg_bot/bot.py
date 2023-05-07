import telebot
from telebot import TeleBot

import utils
from token_storage import get_bot_token

bot: TeleBot = telebot.TeleBot(token=get_bot_token())


def send_message(chat_id, data, keyboard=None):
    try:
        bot.send_message(chat_id=chat_id, text=data, reply_markup=keyboard, parse_mode='HTML')
    except:
        try:
            bot.send_message(chat_id=utils.my_id, text=f"Cant send message for {chat_id} with data {data}")
        except:
            print(f"Cant send message for {chat_id} with data {data}")


def send_log_message(tg_message, info: str):
    bot.send_message(utils.my_id, f"User {tg_message.chat.username}/{tg_message.chat.id} {info}")


def send_log_message_call(call, info: str):
    bot.send_message(utils.my_id, f"User {call.from_user.id} {info}")
