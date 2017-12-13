# coding=UTF-8
from bs4 import BeautifulSoup
import urllib2
import re
import mysqlDb

def getQsbaike():
	url = 'http://news.10jqka.com.cn/realtimenews.html'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	mysl = mysqlDb.Mysql()
	try:
	    request = urllib2.Request(url,headers = headers)
	    response = urllib2.urlopen(request)
	    content = response.read().decode('gbk')
	    print "content",content
	    soup = BeautifulSoup(content, 'html.parser')
	    nodes = soup.find_all('div', class_="newsDetail")
	    print "a标签内容",nodes
	    for node in nodes:
	    	print node
	        content = node.find("span").getText().strip()
	        print "内容:"+content
	        # mysl._insert("qiu",["val"],[content])

	except urllib2.URLError, e:
	    if hasattr(e,"code"):
	        print e.code
	    if hasattr(e,"reason"):
	        print e.reason


getQsbaike()