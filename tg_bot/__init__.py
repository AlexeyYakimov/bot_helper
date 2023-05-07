from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from tg_bot import bot
from tg_bot import keyboards
from tg_bot.keyboards import aqi_btn, puk_btn, inline_aqi_btn, weather_btn, custom_amount_btn


def send_message(chat_id, data, keyboard=None):
    bot.send_message(chat_id, data, keyboard)


def send_log_message(tg_message, info: str):
    bot.send_log_message(tg_message, info)


def send_log_message_call(call, info: str):
    bot.send_log_message_call(call, info)


def get_reply_keyboard() -> ReplyKeyboardMarkup:
    return keyboards.get_reply_keyboard()


def get_inline_keyboard() -> InlineKeyboardMarkup():
    return keyboards.get_inline_keyboard()
