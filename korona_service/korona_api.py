import locale
from typing import Dict, Any

import requests
from requests import RequestException

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}

url = "https://koronapay.com/transfers/online/api/transfers/tariffs"

query_parameters = {
    'sendingCountryId': 'RUS',
    'sendingCurrencyId': 810,
    'receivingCountryId': 'GEO',
    'receivingCurrencyId': 981,
    'paymentMethod': 'debitCard',
    'receivingMethod': 'cash',
    'paidNotificationEnabled': False,
    'receivingAmount': 400000
}

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

max_lari_cap = 4950


def get_rate_for(amount: int) -> dict[str, float]:
    query_parameters['receivingAmount'] = amount * 100
    data = requests.get(url=url, params=query_parameters, headers=headers).json()[0]
    sending_amount = data['sendingAmountWithoutCommission'] / 100
    return {'exchangeRate': data['exchangeRate'], 'amount': sending_amount}


def get_custom_amount(amount: int) -> str:
    try:
        data = get_rate_for(amount)
        return f"Exchange Rate: <b>{data['exchangeRate']}</b>\n\n" \
               f"Pay <b>{get_pretty_amount(data['amount'])}₽</b> for <b>{amount}₾</b>"
    except RequestException:
        print("Error")
        return "Some thing went wrong, try again later!"
    except ValueError as e:
        print(f"Value Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"
    except KeyError as e:
        print(f"Key Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"


def get_pretty_amount(amount) -> str:
    return locale.currency(amount, grouping=True, international=True, symbol=False)
