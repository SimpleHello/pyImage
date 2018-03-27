# coding=UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
import share
import logging
import datetime

logging.basicConfig()


def startIndex():
    now_time = datetime.datetime.now()
    queryTime = now_time + datetime.timedelta(days=-3)
    share.saveHistory(queryTime)

# job = BlockingScheduler()
# # 每天2点执行 生成上一天的历史数据
# # day_of_week 0-6 对应 mon(0),tue(1),wed(2),thu(3),fri(4),sat(5),sun(6)
# job.add_job(startIndex, 'cron', day_of_week='1-5', hour=2)
# job.start()
startIndex()
