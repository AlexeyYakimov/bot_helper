from tg_bot import bot, keyboards


# @tg_bot.bot.bot.message_handler(content_types=['text'])

def start_handler(tbot, message):
    tbot.send_message(chat_id=message.chat.id, text="Hi registered", reply_markup=keyboards.get_reply_keyboard())


def all_text_handler(message):
    try:
        bot.send_message(message.chat.id, "Stop writing to me, i don't understand it:)\n"
                                          "Just push on the buttons under text message field.",
                         keyboard=keyboards.get_reply_keyboard())
    except:
        bot.send_log_message(message, f"cant use {message.text}")
        bot.send_message(message.chat.id, "something went wrong!")


def register_handlers():
    bot.bot.register_message_handler(start_handler, commands=['start'])
    bot.bot.register_message_handler(all_text_handler, content_types=['text'])
