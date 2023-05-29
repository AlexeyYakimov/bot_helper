from schedule_runner.schedule import add_currency_service_to_schedule
from schedule_runner.sheduler import scheduler_run, scheduler_remove_all_tasks


def add_all_tasks():
    add_currency_service_to_schedule()


def run_cron():
    scheduler_run()


def clean_cron():
    scheduler_remove_all_tasks()
