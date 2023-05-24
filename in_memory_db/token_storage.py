import os
from enum import Enum

_token_dict = {}


class Token(Enum):
    TELEGRAM = 'bot'
    NGROK = 'ngrok'
    STORMGLASS = 'stormglass'
    ALERT = 'alert'
    AQI = 'iqair'
    API = 'apitoken',
    API_LAYER = 'apilayer'


def get_token(token: Token) -> str:
    _read_file()
    if len(_token_dict[token.value]) != 0:
        token = _token_dict[token.value]
    else:
        raise Exception(f"Provide your {token.value} token in file with cold api_keys")
    return token


def _read_file():
    if len(_token_dict) == 0:
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        file = open(f'{ROOT_DIR}/api_keys').readlines()
        for line in file:
            pair = line.split("=")
            key = pair[0]
            value = pair[1].replace('\n', "").replace(" ", "")
            if value[0] == '>':
                value = ''

            _token_dict[key] = value
