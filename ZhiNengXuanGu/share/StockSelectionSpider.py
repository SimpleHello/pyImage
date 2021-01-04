# _*_ coding=UTF-8 _*_
import datetime
import urllib.request

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from tool import mysqlDb
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')#设置无页面模式


# 同花顺智能选股网站爬取

def getAiIndex():
    chrome_options = Options()
    # 设置Chrome浏览器禁用PDF和Flash插件,把图片也关掉了。
    profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],
               "plugins.plugins_disabled": ['Adobe Flash Player'],
               "profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", profile)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", profile)
    # 向Options实例中添加禁用扩展插件的设置参数项
    chrome_options.add_argument("--disable-extensions")
    # 添加屏蔽--ignore-certificate-errors提示信息的设置参数项
    chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # 添加浏览器最大化的设置参数项，启动同时最大化窗口
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.binary_location = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"  # 手动指定使用的浏览器位置

    ctime = datetime.datetime.now()
    url = 'http://stock.10jqka.com.cn/api/znxg/index.html'
    print (ctime, '> 开始解析:', url)
    try:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://stock.10jqka.com.cn/api/znxg/index.html')  # 加载网页
        response = driver.page_source  # 获取网页文本
        print(datetime.datetime.now(), "获取数据完成-进行解析工作")
        analyzeDate(response, ctime)
        print (datetime.datetime.now(), '获取实时数据 操作完成')
        driver.quit()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print (e.code)
        if hasattr(e, "reason"):
            print (e.reason)


def getAiHistory(ctime):
    urlh = ctime.strftime('%Y%m%d')
    startTime = ctime.strftime('%Y-%m-%d')
    deleteName(startTime)
    url = 'http://stock.10jqka.com.cn/api/znxg/' + urlh + '.html'
    print (startTime, '> 开始解析:', url)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        analyzeDate(content, ctime)
        print (ctime, '获取 历史数据 操作完成')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print (e.code)
        if hasattr(e, "reason"):
            print (e.reason)


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
                        print ('异常数据:', share, aNode, noStart, '不做处理--')
                    else:
                        mysl._insert("Share_ths_ai_detail",
                                     ['type', 'name', 'code', 'lasts', 'opens', 'ends', 'ranges', 'hour',
                                      'day', 'pop', 'push', 'week'],
                                     [title, share, aNode, "#" + beEnd, "#" + noStart, "#" + noEnd, "#" + amm,
                                      "#" + noHour,
                                      "#" + noDay, "#0", "#0", "#" + str(week)])
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print (e.code)
        if hasattr(e, "reason"):
            print (e.reason)


def getNameValue(name):
    mysl = mysqlDb.Mysql()
    result = mysl.getAll('select count(1) as num from Share_ths_ai_info where name="' + name + '"')
    co = result[0]['num']
    return co


def deleteName(time):
    mysl = mysqlDb.Mysql()
    deleteSql01 = 'delete from Share_ths_ai_succ where ctime= str_to_date("' + time + '", "%Y-%m-%d")'
    print (deleteSql01)
    mysl.delete(deleteSql01)
    return 1
