import tushare as ts
from ZhiNengXuanGu import mysqlDb

mysl = mysqlDb.Mysql()

def getByTime(code):
    mysl = mysqlDb.Mysql()
    con = ts.get_k_data(code, start='2018-03-09', end='2018-03-09')
    xo = con.open.values[0]
    mysl._insert("test20180310", ["amm"], ["#" + str(xo)])
    print 1


getByTime('002012')

# con = ts.get_k_data('002012', start='2018-03-09', end='2018-03-09')
# print con.open
# for inx in con.open:
#     print inx