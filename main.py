import requests
import telebot
from flask import Flask, request

import aqi_service.handlers
import korona_service
import tg_bot
import utils
import weather_service
from token_storage import get_bot_token, get_ngrok_token, get_alert_token

app = Flask(__name__)


def get_webhook_url(ngrok_t, bot_t) -> str:
    try:
        response = requests.get(url="https://api.ngrok.com/endpoints",
                                headers={'Authorization': f"Bearer {ngrok_t}",
                                         'Ngrok-Version': "2"})
        url = response.json()["endpoints"][0]["public_url"]
        return url + "/" + bot_t
    except:
        tg_bot.bot.bot.send_message(utils.my_id, "ngrok down")


@app.route('/' + get_bot_token(), methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    tg_bot.bot.bot.process_new_updates([update])
    return 'ok', 200


@app.route('/alert', methods=['POST'])
def send_alert_to():
    try:
        if request.headers['Authorization'] == get_alert_token():
            json_data = request.get_json()
            id = json_data.get('id', None)
            msg = json_data.get('msg')

            if id is not None:
                tg_bot.bot.bot.send_message(id, msg)
            else:
                tg_bot.bot.bot.send_message(utils.do_id, msg)
                tg_bot.bot.bot.send_message(utils.my_id, msg)

            return {'success': "Alert successfully send"}, 200
        else:
            return {'error': "Sorry wrong token"}, 401
    except:
        return {'error': "Sorry, server temporary down:("}, 500


aqi_service.register_handlers()
korona_service.register_handlers()
weather_service.register_handlers()
tg_bot.register_handlers()

if __name__ == '__main__':
    bot_token = get_bot_token()
    ngrok_token = get_ngrok_token()

    ngrok_url = get_webhook_url(ngrok_t=ngrok_token, bot_t=bot_token)
    tg_bot.bot.bot.remove_webhook()
    # tg_bot.bot.bot.set_webhook(url=ngrok_url)
    tg_bot.bot.bot.infinity_polling()

    tg_bot.bot.bot.send_message(utils.my_id, f"Bot started {ngrok_url} \n\n Alert: {get_alert_token()}")
    # app.run(host='0.0.0.0', port=os.environ.get("PORT", 8081))
