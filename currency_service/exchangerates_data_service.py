import requests

from data_models import CurrencyData
from db.queues import get_currency_by_name, get_currency_by_names
from in_memory_db.token_storage import get_token, Token


# resp_example = {
#     "base": "USD",
#     "date": "2023-05-15",
#     "rates": {
#         "EUR": 0.91932,
#         "GEL": 2.574989,
#         "RUB": 79.288969
#     },
#     "success": True,
#     "timestamp": 1684138863
# }


# 'RateLimit-Limit': '250',
# 'RateLimit-Remaining': '243',
# 'RateLimit-Reset': '1138520',
# 'X-RateLimit-Limit-Day': '250',
# 'X-RateLimit-Limit-Month': '250',
# 'X-RateLimit-Remaining-Day': '248',
# 'X-RateLimit-Remaining-Month': '243',

def get_currency_data(source: str, cur_list: list) -> list:
    names_list = ",".join(cur_list)
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={names_list}&base={source}"
    result = []

    headers = {
        "apikey": f"{get_token(Token.API_LAYER)}"
    }

    response = requests.request("GET", url, headers=headers)
    response = response.json()
    timestamp = response['timestamp']
    base = get_currency_by_name(str(response['base']))

    rates: dict = response['rates']

    keys = get_currency_by_names(rates.keys())

    for c, r in rates.items():
        name = ""
        for n in keys:
            if n.name == c.removeprefix(base.name):
                name = n
        result.append(CurrencyData(timestamp=timestamp,
                                   rate=float(r),
                                   currency=name,
                                   source_currency=base
                                   ))
    return result
