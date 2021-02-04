# _*_ coding=UTF-8 _*_
import datetime
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import psycopg2
from concurrent.futures import ThreadPoolExecutor

chrome_options = Options()
chrome_options.add_argument('--headless')  # 设置无页面模式

# capa = DesiredCapabilities.CHROME
# capa["pageLoadStrategy"] = "none"

conn = psycopg2.connect(database="exam", user="admin", password="123456", host="172.16.6.101", port="5432")
print("Opened database successfully")

# 设置Chrome浏览器禁用PDF和Flash插件,把图片也关掉了。
profile = {"plugins.plugins_disabled": ['Chrome PDF Viewer'],
           "plugins.plugins_disabled": ['Adobe Flash Player'],
           "profile.managed_default_content_settings.images": 2}
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
chrome_options.binary_location = r"C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe"  # 手动指定使用的浏览器位置
driver = webdriver.Chrome(options=chrome_options)


# 同花顺智能选股网站爬取

def getFundIndex(name, ctime, symbol):
    url = 'http://data.eastmoney.com/zlsj/detail/' + ctime + '-0-' + symbol + '.html'
    print(datetime.datetime.now(), '> 开始解析:', url)
    driver.get(url)  # 加载网页
    response = driver.page_source  # 获取网页文本
    print(datetime.datetime.now(), "获取数据完成-进行解析工作")
    analyzeDate(name, symbol, ctime, response)
    print(datetime.datetime.now(), '获取实时数据 操作完成')


def getFundIndexGateway(param):
    getFundIndex(param[0], param[1], param[2])


def analyzeDate(name, symbol, ctime, content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        nodes = soup.find_all('div', id="ccyl")
        for node in nodes:
            pNodes = node.find_all('tbody')
            for pNode in pNodes:
                trNodes = pNode.find_all('tr')
                first = 1
                organ = ''
                organNum = '0'
                stackNum = '0'
                stackMoney = '0'
                rateTotalStack = '0'
                rateCirculateStack = '0'
                for trNode in trNodes:
                    num = 0
                    tdNodes = trNode.find_all('td')
                    for tr in tdNodes:
                        value = tr.getText().strip()
                        if value == '-':
                            value = '0'
                        if num == first:
                            organ = value
                        elif num == first + 1:
                            organNum = value
                        elif num == first + 2:
                            stackNum = value
                        elif num == first + 3:
                            stackMoney = value
                        elif num == first + 4:
                            rateTotalStack = value
                        elif num == first + 5:
                            rateCirculateStack = value
                        num += 1
                    if first == 1:
                        first = 0
                    saveList(name, symbol, ctime, organ, int(organNum), float(stackNum), float(stackMoney),
                             float(rateTotalStack), float(rateCirculateStack))
        # 关闭链接
        conn.commit()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def getBaseList():
    cur = conn.cursor()
    cur.execute("SELECT * from stock_basic where market<> '科创板' and  id > 97 and id<=105")
    return cur.fetchall()


def saveList(name1, symbol1, ctime1, organ1, organNum1, stackNum1, stackMoney1, rateTotalStack1, rateCirculateStack1):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO stock_fund_history2(name,symbol ,ctime ,organ,organNum,stackNum,stackMoney,rateTotalStack,rateCirculateStack)"
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        , (name1, symbol1, ctime1, organ1, organNum1, stackNum1, stackMoney1, rateTotalStack1, rateCirculateStack1))
    print("save successfully", name1, symbol1, ctime1, organ1, organNum1, stackNum1, stackMoney1, rateTotalStack1,
          rateCirculateStack1)


if __name__ == '__main__':
    rows = getBaseList()
    pool = ThreadPoolExecutor(max_workers=20)
    params = []
    for row in rows:
        time.sleep(2)
        print(datetime.datetime.now(), row[3], " ", row[2])
        param = (row[3], '2020-09-30', row[2])
        future1 = pool.submit(getFundIndexGateway,param)

    # getFundIndex('平安银行', '2020-09-30', '000001')
