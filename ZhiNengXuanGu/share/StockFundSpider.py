# _*_ coding=UTF-8 _*_
import datetime
import urllib.request

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')  # 设置无页面模式


# 同花顺智能选股网站爬取

def getFundIndex():
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
    chrome_options.binary_location = r"C:\Users\86158\AppData\Local\Google\Chrome\Application\chrome.exe"  # 手动指定使用的浏览器位置

    ctime = datetime.datetime.now()
    url = 'http://data.eastmoney.com/zlsj/detail/2020-09-30-0-600570.html'
    print(ctime, '> 开始解析:', url)
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)  # 加载网页
        response = driver.page_source  # 获取网页文本
        print(datetime.datetime.now(), "获取数据完成-进行解析工作")
        analyzeDate(response)
        print(datetime.datetime.now(), '获取实时数据 操作完成')
        driver.quit()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def analyzeDate(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        nodes = soup.find_all('div', id="ccyl")
        for node in nodes:
            pNodes = node.find_all('tbody')
            for pNode in pNodes:
                trNodes = pNode.find_all('tr')
                first = 1
                for trNode in trNodes:
                    num = 0
                    tdNodes = trNode.find_all('td')
                    for tr in tdNodes:
                        value = tr.getText().strip()
                        if num == first:
                            print("name:", value)
                        elif num == first + 1:
                            print("count:", value)
                        elif num == first + 2:
                            print("num:", value)
                        elif num == first + 3:
                            print("money:", value)
                        elif num == first + 4:
                            print("rateTotal:", value)
                        elif num == first + 5:
                            print("rateFlow:", value)
                        num += 1
                    if first == 1:
                        first = 0
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


if __name__ == '__main__':
    getFundIndex()
