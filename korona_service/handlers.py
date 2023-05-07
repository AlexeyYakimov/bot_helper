import tg_bot as bot
from korona_service.korona_api import get_custom_amount, max_lari_cap
from tg_bot import custom_amount_btn, puk_btn
from tg_bot.bot import bot as main_bot


def money_handler(message):
    bot.send_message(message.chat.id, get_custom_amount(), keyboard=bot.get_reply_keyboard())
    bot.send_log_message(message, f"use {message.text}")


def custom_amount_handler(message):
    bot.send_message(message.chat.id, "Enter amount in lari ₾:", keyboard=bot.get_reply_keyboard())
    bot.send_log_message(message, f"use {message.text}")
    main_bot.register_next_step_handler(message, amount_handler)


def amount_handler(message):
    if int(message.text) > max_lari_cap:
        main_bot.register_next_step_handler(message, amount_handler)
        bot.send_message(message.chat.id, get_custom_amount(int(message.text)))
    else:
        bot.send_message(message.chat.id, get_custom_amount(int(message.text)), keyboard=bot.get_reply_keyboard())

    bot.send_log_message(message, f"use Custom amount with {message.text}")


def register_handlers():
    main_bot.register_message_handler(money_handler, func=lambda message: message.text == puk_btn,
                                      content_types=['text'])

    main_bot.register_message_handler(custom_amount_handler,
                                      func=lambda message: message.text == custom_amount_btn,
                                      content_types=['text'])
