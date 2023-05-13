import tg_bot as bot
from tg_bot import weather_btn
from tg_bot.keyboards import message_match_button
from weather_service import marine_api


def weather_handler(message):
    data = marine_api.get_formatted_tg_message()
    bot.send_message(message.chat.id, data, user_name=message.chat.username, keyboard=bot.get_reply_keyboard())
    bot.send_log_message(message.chat.id, message.chat.username, message.chat.text)


def register_handlers():
    bot.bot.bot.register_message_handler(weather_handler,
                                         func=lambda message: message_match_button(message.text, weather_btn),
                                         content_types=['text'])
