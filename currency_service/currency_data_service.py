import requests

from currency_service.data_model import CurrencyData
from db.queues import Currency
from in_memory_db.token_storage import get_token, Token

response_example = """{
  "quotes": {
    "USDEUR": 0.914104,
    "USDGEL": 2.57504,
    "USDRUB": 77.360373
  },
  "source": "USD",
  "success": true,
  "timestamp": 1683980043
}"""


def get_currency_data() -> list:
    url = "https://api.apilayer.com/currency_data/live?source=USD&cies=EUR,GEL,RUB"
    result = []
    try:
        headers = {
            "apikey": f"{get_token(Token.API_LAYER)}"
        }

        response = requests.request("GET", url, headers=headers).json()
        timestamp = response['timestamp']
        source = Currency.from_str(str(response['source']))
        print(response)
        rates: dict = response['quotes']

        for c, r in rates.items():
            print(source.name)
            name = Currency.from_str(c.removeprefix(source.name))
            result.append(CurrencyData(timestamp=timestamp,
                                       rate=float(r),
                                       currency=name,
                                       source_currency=source
                                       ))
        return result
    except Exception as e:
        print(f"Some thing broke on {url} {e}")
        return result

if __name__ == '__main__':
    asd = get_currency_data()
    for i in asd:
        print(f"{i.rate} {i.currency}")