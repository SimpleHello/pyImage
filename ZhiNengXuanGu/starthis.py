# coding=UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
import share
import logging
import datetime

logging.basicConfig()


def startIndex():
    now_time = datetime.datetime.now()
    queryTime = now_time + datetime.timedelta(days=-1)
    share.saveHistory(queryTime)


job = BlockingScheduler()
# 每天2点执行
job.add_job(startIndex, 'cron', day_of_week='0-7', hour=2)
job.start()
# startIndex()
