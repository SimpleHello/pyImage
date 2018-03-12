import tushare as ts


def getByTime(code):
    data = ts.get_k_data(code, start='2018-03-09', end='2018-03-09')
    print data
    print '------------------------'
    num = data.index[0]
    print data.loc[num].values[2]


getByTime('000823')
