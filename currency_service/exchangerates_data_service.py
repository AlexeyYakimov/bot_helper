import requests

from data_models import CurrencyData, Currency
from in_memory_db.token_storage import get_token, Token


# resp_example = """{
#   "base": "USD",
#   "date": "2023-05-15",
#   "rates": {
#     "EUR": 0.91932,
#     "GEL": 2.574989,
#     "RUB": 79.288969
#   },
#   "success": true,
#   "timestamp": 1684138863
# }"""

# 'RateLimit-Limit': '250',
# 'RateLimit-Remaining': '243',
# 'RateLimit-Reset': '1138520',
# 'X-RateLimit-Limit-Day': '250',
# 'X-RateLimit-Limit-Month': '250',
# 'X-RateLimit-Remaining-Day': '248',
# 'X-RateLimit-Remaining-Month': '243',

def get_currency_data() -> list:
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB,GEL,EUR&base=USD"
    result = []

    headers = {
        "apikey": f"{get_token(Token.API_LAYER)}"
    }

    response = requests.request("GET", url, headers=headers)
    print(response.headers)
    response = response.json()
    timestamp = response['timestamp']
    source = Currency.from_str(str(response['base']))

    rates: dict = response['rates']

    for c, r in rates.items():
        name = Currency.from_str(c.removeprefix(source.name))
        result.append(CurrencyData(timestamp=timestamp,
                                   rate=float(r),
                                   currency=name,
                                   source_currency=source
                                   ))
    return result
