import requests

from data_models import CurrencyData, Currency
from db.queues import get_currency_by_name, get_currency_by_names
from in_memory_db.token_storage import get_token, Token

#
# response_example = {
#   "quotes": {
#     "USDEUR": 0.914104,
#     "USDGEL": 2.57504,
#     "USDRUB": 77.360373
#   },
#   "source": "USD",
#   "success": True,
#   "timestamp": 1683980043
# }

# 'RateLimit-Limit': '100',
# 'RateLimit-Remaining': '82',
# 'RateLimit-Reset': '1138520',
# 'X-RateLimit-Limit-Day': '100',
# 'X-RateLimit-Limit-Month': '100',
# 'X-RateLimit-Remaining-Day': '87',
# 'X-RateLimit-Remaining-Month': '82',


def get_currency_data(source, cur_list: list) -> list:
    names_list = ",".join(cur_list)
    url = f"https://api.apilayer.com/currency_data/live?source={source}&currencies={names_list}"
    result = []
    headers = {
        "apikey": f"{get_token(Token.API_LAYER)}"
    }

    response = requests.request("GET", url, headers=headers).json()
    timestamp = response['timestamp']
    base = get_currency_by_name(str(response['source']))
    rates: dict = response['quotes']

    mapped = list(map(lambda k: k.removeprefix(base.name), rates.keys()))
    print(mapped)
    cur_l = get_currency_by_names(mapped)
    print(cur_l)
    for key, value in rates.items():
        current_cur = None
        for n in cur_l:
            if n.name == key.removeprefix(base.name):
                current_cur = n

        result.append(CurrencyData(timestamp=timestamp,
                                   rate=float(value),
                                   currency=current_cur,
                                   source_currency=base
                                   ))
    return result
