import tg_bot as bot
from aqi_service import iquair_service as aqi
from tg_bot import aqi_btn, inline_aqi_btn


def aqi_message_handler(message):
    bot.send_message(message.chat.id, aqi.get_data(), keyboard=bot.get_inline_keyboard())
    bot.send_log_message(message, f"use {message.text}")


def aqi_description_handler(call):
    bot.send_message(call.from_user.id, aqi.get_description(), keyboard=bot.get_reply_keyboard())
    bot.send_log_message_call(call, f"use {call.data}")


def register_handlers():
    bot.bot.bot.register_message_handler(aqi_message_handler,
                                         func=lambda message: message.text == aqi_btn,
                                         content_types=['text'])

    bot.bot.bot.register_callback_query_handler(aqi_description_handler,
                                                func=lambda call: call.data == inline_aqi_btn)
