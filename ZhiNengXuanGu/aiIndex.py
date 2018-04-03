# _*_ coding=UTF-8 _*_
import urllib2
import datetime
import mysqlDb
import Config
from bs4 import BeautifulSoup
from selenium import webdriver


def getAiIndex():
    ctime = datetime.datetime.now()
    url = 'http://stock.10jqka.com.cn/api/znxg/index.html'
    print ctime, '> 开始解析:', url
    try:
        if Config.PhantomJS is None:
            driver = webdriver.PhantomJS()
        else:
            driver = webdriver.PhantomJS(Config.PhantomJS)
        driver.get('http://stock.10jqka.com.cn/api/znxg/index.html')  # 加载网页
        response = driver.page_source  # 获取网页文本
        content = response.decode('utf-8')
        analyzeDate(content, ctime)
        print ctime, '获取实时数据 操作完成'
        driver.quit()
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


def getAiHistory(ctime):
    urlh = ctime.strftime('%Y%m%d')
    startTime = ctime.strftime('%Y-%m-%d')
    deleteName(startTime)
    url = 'http://stock.10jqka.com.cn/api/znxg/' + urlh + '.html'
    print startTime, '> 开始解析:', url
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        analyzeDate(content, ctime)
        print ctime, '获取 历史数据 操作完成'
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


def analyzeDate(content, ctime):
    try:
        noHour = ctime.strftime('%H')
        noDay = ctime.strftime('%Y%m%d')
        startTime = ctime.strftime('%Y-%m-%d %H:%M')
        # 对应 mon(0),tue(1),wed(2),thu(3),fri(4),sat(5),sun(6)
        week = ctime.weekday()
        mysl = mysqlDb.Mysql()
        soup = BeautifulSoup(content, 'html.parser')
        nodes = soup.find_all('div', class_="screen clearfix")
        for node in nodes:
            pNodes = node.find_all('p')
            title = node.find('h1').getText().strip()
            title = title.replace("查看全部", "").strip()
            col = 1
            if title.startswith('创新高') or title.startswith('连续上涨'):
                continue
            else:
                if getNameValue(title) == 0: col = 0

            for pNode in pNodes:
                detail = pNode.getText().strip()
                if detail.startswith('【综合成功率】'):
                    succ = detail.replace("【综合成功率】", "").replace("\n", "").strip()
                    succ = succ[0:succ.index('%选出')]
                    mysl._insert("Share_ths_ai_succ", ["name", 'succ', 'ctime'], [title, "#" + succ, startTime])
                elif detail.startswith('【核心用法】') and col == 0:
                    mysl._insert("Share_ths_ai_info", ["name", 'detail'], [title, detail])
            tableNodes = node.find_all('table', class_="screen-table J_screenTable")
            for tableNode in tableNodes:
                trNodes = tableNode.find_all('tr')
                for tr in trNodes:
                    aNode = tr.find('a')['data-code']
                    trNodes = tr.find_all('td')
                    share = ''
                    num = 0
                    beEnd = 0
                    noStart = 0
                    noEnd = 0
                    amm = 0
                    for tr in trNodes:
                        value = tr.getText().strip()
                        if num == 0:
                            share = value
                        elif num == 1:
                            noEnd = value
                        elif num == 2:
                            amm = value.replace("%", "").strip()
                        elif num == 3:
                            noStart = value
                        elif num == 4:
                            beEnd = value
                        num += 1
                    innoStart = float(noStart)
                    if innoStart > 500:
                        print '异常数据:', share, aNode, noStart, '不做处理--'
                    else:
                        mysl._insert("Share_ths_ai_detail",
                                     ['type', 'name', 'code', 'lasts', 'opens', 'ends', 'range', 'hour',
                                      'day', 'pop', 'push', 'week'],
                                     [title, share, aNode, "#" + beEnd, "#" + noStart, "#" + noEnd, "#" + amm,
                                      "#" + noHour,
                                      "#" + noDay, "#0", "#0", "#" + str(week)])
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


def getNameValue(name):
    mysl = mysqlDb.Mysql()
    result = mysl.getAll('select count(1) as num from Share_ths_ai_info where name="' + name + '"')
    co = result[0]['num']
    return co


def deleteName(time):
    mysl = mysqlDb.Mysql()
    deleteSql01 = 'delete from Share_ths_ai_succ where ctime= str_to_date("' + time + '", "%Y-%m-%d")'
    print deleteSql01
    mysl.delete(deleteSql01)
    return 1
