# coding=UTF-8
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig()


def startIndex():
    CheckService.getNa()

if __name__ == '__main__':
    job = BlockingScheduler()
    # day_of_week 0-6 对应 mon(0),tue(1),wed(2),thu(3),fri(4),sat(5),sun(6)
    job.add_job(startIndex, 'cron', minute='20', hour='8,22', day_of_week='0-6')
    job.start()


