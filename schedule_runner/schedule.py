from currency_service import service100, service250
from db.queues import save_currency_data_list, save_korona_data
from korona_service import get_korona_amount_for
from schedule_runner.sheduler import add_task


def currency_task_100():
    data = service100("USD",
                      ["EUR", "RUB", "GEL", "AMD", "UAH", "TRY", "SGD", "SEK", "RSD", "RON", "PLN", "MXN", "LVL", "LTL",
                       "JPY",
                       "HUF", "CZK", "CNY", "CHF", "BGN", "AED", "AUD", "ALL", "UZS"])
    save_currency_data_list(data)


def currency_task_250():
    data = service250("USD",
                      ["EUR", "RUB", "GEL", "AMD", "UAH", "TRY", "SGD", "SEK", "RSD", "RON", "PLN", "MXN", "LVL", "LTL",
                       "JPY",
                       "HUF", "CZK", "CNY", "CHF", "BGN", "AED", "AUD", "ALL", "UZS"])
    save_currency_data_list(data)


def korona_task():
    data = get_korona_amount_for(1000)
    save_korona_data(data)


def add_currency_service_to_schedule():
    add_task(currency_task_250, hours='8,10,12,14,16,18,20,23', minute=1)
    add_task(currency_task_100, hours='11,17,22', minute=2)
    add_task(korona_task, hours='8-23', minute='5,35')
