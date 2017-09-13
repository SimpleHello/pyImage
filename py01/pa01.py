# coding=UTF-8
from bs4 import BeautifulSoup
import urllib2
import re
import mysqlDb

def getQsbaike(page):
	url = 'http://www.qiushibaike.com/hot/page/' + str(page)
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	mysl = mysqlDb.Mysql()
	try:
	    request = urllib2.Request(url,headers = headers)
	    response = urllib2.urlopen(request)
	    content = response.read().decode('utf-8')
	    soup = BeautifulSoup(content, 'html.parser')
	    nodes = soup.find_all('div', class_="article block untagged mb15 typs_hot")
	    for node in nodes:
	        content = node.find('div', class_="content").find("span").getText().strip()
	        print content
	        mysl._insert("qiu",["val"],[content])

	except urllib2.URLError, e:
	    if hasattr(e,"code"):
	        print e.code
	    if hasattr(e,"reason"):
	        print e.reason
