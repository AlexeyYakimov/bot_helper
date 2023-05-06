my_id = 228642352
do_id = 85363124

TZ_GE = 'Asia/Tbilisi'
TZ_UTC = 'UTC'


def remove_key_safe(dictionary: dict, key) -> bool:
    try:
        dictionary.pop(key)
        return True
    except KeyError:
        return False


def send_log_message(bot, tg_message, info: str):
    bot.send_message(my_id, f"User {tg_message.chat.username}/{tg_message.chat.id} {info}")


def send_log_message_call(bot, call, info: str):
    bot.send_message(my_id, f"User {call.from_user.id} {info}")
