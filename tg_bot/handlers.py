from tg_bot import bot, keyboards


def start_handler(message):
    bot.send_message(chat_id=message.chat.id, data="Hi registered", keyboard=keyboards.get_reply_keyboard())


def all_text_handler(message):
    try:
        bot.send_message(message.chat.id, "Stop writing to me, i don't understand it:)\n"
                                          "Just push on the buttons under text message field.",
                         keyboard=keyboards.get_reply_keyboard())
    except:
        bot.send_message(message.chat.id, "something went wrong!")


def register_handlers():
    bot.bot.register_message_handler(start_handler, commands=['start'])
    bot.bot.register_message_handler(all_text_handler, content_types=['text'])
