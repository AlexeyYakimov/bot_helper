from currency_service.currency_data_service import get_currency_data as service100
from currency_service.exchangerates_data_service import get_currency_data as service250
from db.queues import save_currency_data_list
from schedule_runner.sheduler import add_task


def currency_task_100():
    print("Run 100")
    data = service100("USD",
                      ["EUR", "RUB", "GEL", "AMD", "UAH", "TRY", "SGD", "SEK", "RSD", "RON", "PLN", "MXN", "LVL", "LTL",
                       "JPY",
                       "HUF", "CZK", "CNY", "CHF", "BGN", "AED", "AUD", "ALL", "UZS"])
    save_currency_data_list(data)


def currency_task_250():
    print("Run 250")
    data = service250("USD",
                      ["EUR", "RUB", "GEL", "AMD", "UAH", "TRY", "SGD", "SEK", "RSD", "RON", "PLN", "MXN", "LVL", "LTL",
                       "JPY",
                       "HUF", "CZK", "CNY", "CHF", "BGN", "AED", "AUD", "ALL", "UZS"])
    save_currency_data_list(data)


def add_currency_service_to_schedule():
    add_task(currency_task_250, hours='8,10,12,14,16,18,20,23', minute='0')
    add_task(currency_task_100, hours='11,17,22', minute='0')
