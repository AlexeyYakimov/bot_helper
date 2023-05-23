import datetime
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def add_task(func, hours, minute):
    scheduler.add_job(func=func,
                      trigger='cron',
                      hour=hours,
                      minute=minute,
                      timezone='Asia/Tbilisi')


def scheduler_run():
    scheduler.start()
