import locale

import requests

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


def get_custom_amount(amount: int = 4000) -> str:
    query_parameters['receivingAmount'] = amount * 100
    try:
        data = requests.get(url=url, params=query_parameters, headers=headers).json()[0]
        sending_amount = data['sendingAmountWithoutCommission'] / 100
        return f"Exchange Rate: {data['exchangeRate']}\n\nFor {amount}₾ you payed {get_pretty_amount(sending_amount)}₽"
    except:
        return "Wou wou wou, easy, enter sum less then 4900₾"


def get_pretty_amount(amount) -> str:
    return locale.currency(amount, grouping=True, international=True, symbol=False)
