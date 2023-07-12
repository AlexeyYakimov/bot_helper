import logging

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

flask = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

scheduler = BackgroundScheduler(job_defaults={'coalesce': False,
                                              'max_instances': 4}
                                )


def add_task(func, hours, minute):
    scheduler.add_job(func=func,
                      id=func.__name__,
                      trigger='cron',
                      hour=hours,
                      minute=minute,
                      timezone='Asia/Tbilisi',
                      replace_existing=True)


def my_listener(event):
    if event.exception:
        print('The job crashed :(')
        print(f"{scheduler.get_jobs()}")
    else:
        print('The job worked :)')


def scheduler_run():
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()


def scheduler_remove_all_tasks():
    scheduler.remove_all_jobs()
