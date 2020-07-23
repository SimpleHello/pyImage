# _*_ coding=UTF-8 _*_
#基于 python3 完成
import urllib.request
import requests
from bs4 import BeautifulSoup
import codecs


def getAiIndex(ctime):
    url = 'https://www.ssydt.com/article/'+ctime
    # print (ctime, '> 开始解析:', url)
    try:
        content = requests.get(url)  # 加载网页
        soup = BeautifulSoup(content.text,features='html.parser')
        analyzeDate(soup)
    except urllib.error.URLError as  e:
        if hasattr(e, "code"):
            print (e.code)
        if hasattr(e, "reason"):
            print (e.reason)


def analyzeDate(soup):
    path = "test12.txt"
    try:
        nodes = soup.find_all('div', class_="article-content")
        for node in nodes:
            pNodes = node.find_all('p', class_="MsoNormal")
            for pNode in pNodes:
                context = pNode.getText().strip();
                if context=='国际：':
                    break
                if context == '国内：':
                    continue
                writetxt(path,context)
                print("写入", context)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)



def writetxt(path, content):
    with codecs.open(path, 'a', encoding='utf-8')as f:
        f.write(content + "\n")