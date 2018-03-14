# coding=UTF-8
from apscheduler.schedulers.blocking import BlockingScheduler
import aiIndex
import logging

logging.basicConfig()


def startIndex():
    aiIndex.getAiIndex()


job = BlockingScheduler()
job.add_job(startIndex, 'cron', hour='8,9,12,14,15,18,20')
job.start()
#startIndex()