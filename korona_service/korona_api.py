import locale

import arrow
import requests
from requests import RequestException

from data_models import KoronaData
from db.queues import get_currency_by_name, get_last_korona_data
from in_memory_db.in_memory_data import TZ_CURRENT
from korona_service.utils import calculate_amount

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
    'receivingAmount': 100000
}

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

max_lari_cap = 4950


def _get_korona_data(amount: int) -> KoronaData:
    query_parameters['receivingAmount'] = amount * 100
    data = requests.get(url=url, params=query_parameters, headers=headers).json()[0]
    sending_amount = data['sendingAmountWithoutCommission'] / 100
    sending_currency = get_currency_by_name(data['sendingCurrency']['code'])
    receiving_currency = get_currency_by_name(data['receivingCurrency']['code'])
    return KoronaData(
        int(arrow.now(TZ_CURRENT).timestamp()),
        data['exchangeRate'],
        sending_amount=sending_amount,
        sending_currency=sending_currency,
        receiving_amount=amount,
        receiving_currency=receiving_currency,
        commission=data['sendingCommission']
    )


def get_pretty_print_data(amount: int) -> str:
    try:
        data = calculate_amount(get_last_korona_data(), amount)

        return f"Exchange Rate: <b>{data.rate}</b> on {arrow.get(data.timestamp).to(TZ_CURRENT).strftime('%H:%M')}\n\n" \
               f"Pay <b>{pretty_print(data.sending_amount)}₽</b> for <b>{data.receiving_amount}₾</b>"
    except RequestException:
        print("Error")
        return "Some thing went wrong, try again later!"
    except ValueError as e:
        print(f"Value Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"
    except KeyError as e:
        print(f"Key Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"


def pretty_print(number) -> str:
    moda = divmod(number, 1000)
    result = ""
    for idx, i in enumerate(moda):
        if idx != len(moda) - 1:
            result += f"{int(i)} "
        else:
            result += str(round(i, 2))
    return result
