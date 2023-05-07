import tg_bot as bot
from tg_bot import weather_btn
from weather_service import marine_api


# @tg_bot.bot.bot.message_handler(func=lambda message: message.text == button_weather, content_types=['text'])
def weather_handler(message):
    data = marine_api.get_data_message()
    bot.send_message(message.chat.id, data, keyboard=bot.get_reply_keyboard())
    bot.send_log_message(message, f"use {message.text}")


def register_handlers():
    bot.bot.bot.register_message_handler(weather_handler, func=lambda message: message.text == weather_btn,
                                         content_types=['text'])
