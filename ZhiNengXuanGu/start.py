# coding=UTF-8
import zhineng
import datetime

day = datetime.datetime.now()
for i in range(1, 3):
    yes_time = day + datetime.timedelta(days=-i)
    zhineng.getZhiNeng(yes_time)
