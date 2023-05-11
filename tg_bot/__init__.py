from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from tg_bot import bot, handlers
from tg_bot import keyboards
from tg_bot.bot import bot as main_bot
from tg_bot.keyboards import aqi_btn, puk_btn, inline_aqi_btn, weather_btn, custom_amount_btn
from tg_bot.utils import get_webhook_url
from utils import global_utils
from utils.token_storage import Token, get_token


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
    ngrok_token = get_token(Token.NGROK)

    ngrok_url = get_webhook_url(ngrok_t=ngrok_token, bot_t=bot_token)
    main_bot.remove_webhook()
    main_bot.set_webhook(url=ngrok_url)

    bot.send_message(global_utils.my_id, f"Bot started {ngrok_url} \n\n Alert: {get_token(Token.ALERT)}")
