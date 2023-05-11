from telebot import types

puk_btn = 'Puk'
weather_btn = 'Weather'
custom_amount_btn = 'Enter custom amount'
aqi_btn = "AQI Batumi"

inline_aqi_btn = "Aqi description"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(types.KeyboardButton(puk_btn), types.KeyboardButton(weather_btn))
markup.add(types.KeyboardButton(custom_amount_btn), types.KeyboardButton(aqi_btn))

aqi_description_inline_btn = types.InlineKeyboardButton(text=inline_aqi_btn,
                                                        callback_data=inline_aqi_btn)
inline_keyboard = types.InlineKeyboardMarkup()
inline_keyboard.add(aqi_description_inline_btn)


def message_match_button(message: str, button: str) -> bool:
    return message.lower() == button.lower()


def get_reply_keyboard() -> types.ReplyKeyboardMarkup:
    return markup


def get_inline_keyboard() -> types.InlineKeyboardMarkup():
    return inline_keyboard
