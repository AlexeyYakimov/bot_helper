import logging

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MAX_INSTANCES
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from tg_bot.bot import send_log_message

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
                      misfire_grace_time= 20000,
                      replace_existing=True)


def my_listener(event):
    if event.exception:
        send_log_message(0, "Job crashed!!")
    else:
        print('The job worked :)')


def scheduler_run():
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MAX_INSTANCES)
    scheduler.start()


def scheduler_remove_all_tasks():
    scheduler.remove_all_jobs()
