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

max_lari_cap = 1000000


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
               f"Pay <b>{currency_format(data.sending_amount)}₽</b> for <b>{data.receiving_amount}₾</b>"
    except RequestException:
        print("Error")
        return "Some thing went wrong, try again later!"
    except ValueError as e:
        print(f"Value Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"
    except KeyError as e:
        print(f"Key Error {e}")
        return f"Wou wou wou, easy, enter sum less then <b>{max_lari_cap}₾</b>"


def currency_format(currency) -> str:
    temp = str(currency).split(".")
    result = ""
    for idx, i in enumerate(temp[0][::-1]):
        if idx != 0 and divmod(idx, 3)[1] == 0:
            result = " ".join((i, result))
        else:
            result = "".join((i, result))

    rest = temp[1][:2]
    if len(rest) == 1:
        rest += "0"

    return f"{result}.{rest}"
