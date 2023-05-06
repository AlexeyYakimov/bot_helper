import os

_token_dict = {}


def get_bot_token() -> str:
    _read_file()
    if len(_token_dict['bot']) != 0:
        token = _token_dict['bot']
    else:
        raise Exception("Provide your bot token in file with cold api_keys")
    return token


def get_ngrok_token() -> str:
    _read_file()
    if len(_token_dict['ngrok']) != 0:
        token = _token_dict['ngrok']
    else:
        raise Exception("Provide your ngrok token in file with cold api_keys")
    return token


def get_stormglass_token() -> str:
    _read_file()
    if len(_token_dict['stormglass']) != 0:
        token = _token_dict['stormglass']
    else:
        raise Exception("Provide your stormglass token in file with cold api_keys")
    return token


def get_alert_token() -> str:
    _read_file()
    if len(_token_dict['alert']) != 0:
        token = _token_dict['alert']
    else:
        raise Exception("Provide your alert token in file with cold api_keys")
    return token


def get_iqair_token() -> str:
    _read_file()
    if len(_token_dict['iqair']) != 0:
        token = _token_dict['iqair']
    else:
        raise Exception("Provide your iqair token in file with cold api_keys")
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
