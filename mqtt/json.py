#!/usr/bin/python
# -*- coding: UTF-8 -*-
#python 2解决中文轮码
#import sys
#reload(sys) 
#sys.setdefaultencoding("UTF-8")
#with open('send_dev_datas.xml', 'w') as f:

#python 3解决中文轮码
#with open('send_dev_datas.xml', 'w',encoding='utf-8') as f:
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import xlrd
data = xlrd.open_workbook('alarmModel2.xlsx')
table = data.sheet_by_index(1)
enable = True
highRateT = 0
highRateI = 0
delay = 0
recoverDelay = 0
with open('alarmModel.txt', 'w') as f:
    for i in range(2,table.nrows):
        devType = table.cell(i, 1).value
        alarmId = table.cell(i, 2).value
        colId = table.cell(i, 10).value
        delay = table.cell(i, 12).value
        recoverDelay = table.cell(i, 13).value
        thresholdFlag = table.cell(i, 7).value
        threshold = table.cell(i, 6).value
        if( table.cell(i,6).value != 1 ):
            enable = 'false'
        else:
            enable = 'true'

        message = '"devType" : {0},"alarmId" : "{1}","coId" : "{2}","enable" : {3},"thresholdFlag" : {4}, ' \
                  '"threshold" : {5},"highRateT" :{6},"highRateI" : {7},"delay" : {8},"recoverDelay" : {9}'.format(int(devType),alarmId,colId,enable,int(thresholdFlag),int(threshold),highRateT,highRateI,int(delay),int(recoverDelay))

        message = "{"+message+"}"

        f.write(message)
            
          
 
