# _*_ coding:utf-8 _*_
import tushare as ts
import mysqlDb

mysql = mysqlDb.Mysql()


def saveHistory(queryTime):
    noDay = queryTime.strftime('%Y%m%d')
    times = queryTime.strftime('%Y-%m-%d')
    addCodeExistThs(noDay)
    codes = getCode()
    if codes is False:
        print '当前:', times, '无数据产生'
        return
    for code in codes:
        try:
            code = code['code']
            delCodeExist(code, noDay)
            data = ts.get_k_data(code, start=times, end=times)
            num = data.index[0]
            day = noDay
            st = data.loc[num].values[1]
            en = data.loc[num].values[2]
            amm = round(((en - st) * 100) / st, 2)
            if amm > 10:
                amm = 10
            mysql._insert("Share_ths_ai_his",
                          ['code', 'starts', 'ends', 'range', 'day'],
                          [code, "#" + str(st), "#" + str(en), "#" + str(amm), "#" + day])
            print 'code:', code, '保存成功'

        except BaseException, e:
            print e.message
            print times, code, '出现异常 !!!'


def getCode():
    result = mysql.getAll('select code from Share_ths group by code')
    return result


def addCodeExistThs(queryTime):
    sql = 'INSERT INTO Share_ths(share,code) ' + \
          'SELECT t1.share,t1.code ' + \
          'FROM ' + \
          '(SELECT share,code FROM Share_ths_ai_detail WHERE noDay="' + queryTime + '" GROUP BY  share,code) t1 ' + \
          'WHERE NOT EXISTS (SELECT * FROM Share_ths t2 WHERE t2.share=t1.share AND t2.code = t1.code)'
    mysql.getAll(sql)


def delCodeExist(code, queryTime):
    mysql.getAll('delete from Share_ths_ai_his where day=' + queryTime + ' and code="' + code + '"')


def getByTime(code):
    data = ts.get_k_data(code, start='2018-03-09', end='2018-03-09')
    print data
    print '------------------------'
    num = data.index[0]
    print data.loc[num].values[2]
