from tg_bot import bot, keyboards


def start_handler(message):
    bot.send_message(chat_id=message.chat.id, data="Hi", user_name=message.chat.username,
                     keyboard=keyboards.get_reply_keyboard())
    bot.send_log_message(message.chat.id, message.chat.username, message.chat.text)


def all_text_handler(message):
    try:
        bot.send_message(message.chat.id, "Stop writing to me, i don't understand it:)\n"
                                          "Just push on the buttons under text message field.",
                         user_name=message.chat.username,
                         keyboard=keyboards.get_reply_keyboard())
        bot.send_log_message(message.chat.id, message.chat.username, message.chat.text)
    except:
        bot.send_message(message.chat.id, "something went wrong!", user_name=message.chat.username)
        bot.send_log_message(message.chat.id, message.chat.username, f" broken {message.chat.text}")


def register_handlers():
    bot.bot.register_message_handler(start_handler, commands=['start'])
    bot.bot.register_message_handler(all_text_handler, content_types=['text'])
