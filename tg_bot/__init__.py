import os

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from in_memory_db.in_memory_data import my_id
from in_memory_db.token_storage import Token, get_token
from tg_bot import bot, handlers
from tg_bot import keyboards
from tg_bot.bot import bot as main_bot
from tg_bot.keyboards import aqi_btn, puk_btn, inline_aqi_btn, weather_btn, custom_amount_btn


def send_message(chat_id, data, keyboard=None):
    bot.send_message(chat_id, data, keyboard)


def get_reply_keyboard() -> ReplyKeyboardMarkup:
    return keyboards.get_reply_keyboard()


def get_inline_keyboard() -> InlineKeyboardMarkup():
    return keyboards.get_inline_keyboard()


def register_handlers():
    handlers.register_handlers()


def set_webhook():
    bot_token = get_token(Token.TELEGRAM)
    proxy_domain = os.environ.get("PROXY_DOMAIN", "")

    proxy_url = f"https://{proxy_domain}.loca.lt/"
    main_bot.remove_webhook()
    main_bot.set_webhook(url=proxy_url + bot_token)

    bot.send_message(my_id, f"Bot started {proxy_url} \n\n Alert: {get_token(Token.ALERT)}")
