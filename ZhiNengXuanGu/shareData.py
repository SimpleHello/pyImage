# _*_ coding:utf-8 _*_
import tushare as ts


def saveData():
    try:
        code = '600734'
        data = ts.get_realtime_quotes(code)
        xi = data[['code', 'name', 'price', 'a1_v', 'time']]
        print xi
        print '----------------------'
        print xi.loc[0].values[0]
    except BaseException, e:
        print e.message
