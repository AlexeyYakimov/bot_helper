from threading import Thread

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def add_task(func, hours, minute):
    scheduler.add_job(func=func,
                      trigger='cron',
                      hour=hours,
                      minute=minute,
                      timezone='Asia/Tbilisi')


def scheduler_run():
    Thread(target=scheduler.start).start()


def scheduler_remove_all_tasks():
    scheduler.remove_all_jobs()
