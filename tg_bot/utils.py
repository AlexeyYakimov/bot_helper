import requests

from in_memory_db.in_memory_data import my_id
from tg_bot.bot import bot


def get_webhook_url(ngrok_t, bot_t) -> str:
    try:
        response = requests.get(url="https://api.ngrok.com/endpoints",
                                headers={'Authorization': f"Bearer {ngrok_t}",
                                         'Ngrok-Version': "2"})
        url = response.json()["endpoints"][0]["public_url"]
        return url + "/" + bot_t
    except:
        bot.send_message(my_id, "ngrok down")
