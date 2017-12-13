# _*_ coding:utf-8 _*_

import copy

def getshui():	
	for i in range(100,1000):
		x = i/100 #取得百位
		y = i%100/10  #取得个位数
		z = i%10 #取得个位数
		le = x*x*x+y*y*y+z*z*z
		if le==i:
			print i

def getYin(n):
	for i in range(2,n+1):
		if n%i==0:
			print i,"*",
			return getYin(n/i)
			
getYin(77)
print "你好: %d-%d-%d " % (1,2,3)