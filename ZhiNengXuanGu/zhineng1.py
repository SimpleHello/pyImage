# _*_ coding=UTF-8 _*_
import json
import sys
import datetime
from ZhiNengXuanGu import mysqlDb

mysl = mysqlDb.Mysql()


def getNameValue(name):
    result = mysl.getAll('select count(1) as ni from Share_ths_ai_info where name="' + name + '"')
    co = result[0]['ni']
    if co > 0:
        return True
    else:
        return False


def deleteName(time):
    mysl = mysqlDb.Mysql()
    deleteSql01 = 'delete from Share_ths_ai_detail where ctime= str_to_date("' + time + '", "%Y-%m-%d")'
    mysl.delete(deleteSql01)
    deleteSql01 = 'delete from Share_ths_ai_succ where ctime= str_to_date("' + time + '", "%Y-%m-%d")'
    mysl.delete(deleteSql01)
    return 1


day = datetime.datetime.now()
yes_time = day + datetime.timedelta(days=-1)
timex = yes_time.strftime('%Y-%m-%d')

test = "52%选出3只股票"
print test[0:test.index('选出')]
