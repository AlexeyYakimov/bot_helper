import tg_bot as bot
from aqi_service import iquair_service as aqi
from tg_bot import aqi_btn, inline_aqi_btn
from tg_bot.keyboards import message_match_button


def aqi_message_handler(message):
    bot.send_message(message.chat.id, aqi.get_data(), user_name=message.chat.username,
                     keyboard=bot.get_inline_keyboard())
    bot.send_log_message(message.chat.id, message.chat.username, message.chat.text)


def aqi_description_handler(call):
    bot.send_message(call.from_user.id, aqi.get_description(), user_name=call.from_user.username,
                     keyboard=bot.get_reply_keyboard())
    bot.send_log_message(call.from_user.id, call.from_user.username, call.data)


def register_handlers():
    bot.bot.bot.register_message_handler(aqi_message_handler,
                                         func=lambda message: message_match_button(message.text, aqi_btn),
                                         content_types=['text'])

    bot.bot.bot.register_callback_query_handler(aqi_description_handler,
                                                func=lambda call: message_match_button(call.data, inline_aqi_btn))
