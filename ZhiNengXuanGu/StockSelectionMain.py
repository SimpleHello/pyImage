# coding=UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
import StockSelectionSpider
import logging

logging.basicConfig()


def startIndex():
    StockSelectionSpider.getAiIndex()


job = BlockingScheduler()
# day_of_week 0-6 对应 mon(0),tue(1),wed(2),thu(3),fri(4),sat(5),sun(6)
job.add_job(startIndex, 'cron',minute='40', hour='9,12,15,18', day_of_week='0-4')
job.start()
# startIndex()
