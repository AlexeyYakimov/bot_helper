from currency_service import currency_data_service
from currency_service import exchangerates_data_service


def service100(source, cur_list: list):
    currency_data_service.get_currency_data(source, cur_list)


def service250(source: str, cur_list: list):
    exchangerates_data_service.get_currency_data(source, cur_list)
