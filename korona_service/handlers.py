import tg_bot as bot
from korona_service.korona_api import get_pretty_print_data, max_lari_cap
from tg_bot import custom_amount_btn, puk_btn
from tg_bot.bot import bot as main_bot
from tg_bot.keyboards import message_match_button


def money_handler(message):
    bot.send_message(message.chat.id, get_pretty_print_data(3000), keyboard=bot.get_reply_keyboard())


def custom_amount_handler(message):
    bot.send_message(message.chat.id, "Enter amount in lari ₾:", keyboard=bot.get_reply_keyboard())
    main_bot.register_next_step_handler(message, amount_handler)


def amount_handler(message):
    try:
        if int(message.text) > max_lari_cap:
            main_bot.register_next_step_handler(message, amount_handler)
            bot.send_message(message.chat.id, get_pretty_print_data(int(message.text)))
        else:
            bot.send_message(message.chat.id, get_pretty_print_data(int(message.text)), keyboard=bot.get_reply_keyboard())

    except:
        main_bot.register_next_step_handler(message, amount_handler)
        bot.send_message(message.chat.id, f"Enter only numbers less than {max_lari_cap}₾")


def register_handlers():
    main_bot.register_message_handler(money_handler, func=lambda message: message_match_button(message.text, puk_btn),
                                      content_types=['text'])

    main_bot.register_message_handler(custom_amount_handler,
                                      func=lambda message: message_match_button(message.text, custom_amount_btn),
                                      content_types=['text'])
