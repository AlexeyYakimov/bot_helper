import os
from enum import Enum

_token_dict = {}


class Token(Enum):
    TELEGRAM = 'TELEGRAM_TOKEN'
    NGROK = 'NGROK_API_TOKEN'
    STORMGLASS = 'STORMGLASS_TOKEN'
    ALERT = 'ALERT_TOKEN'
    AQI = 'AQI_TOKEN'
    API = 'API_TOKEN',
    API_LAYER = 'API_LAYER_TOKEN'


def get_token(token: Token) -> str:
    return os.environ.get(token.value, "")
