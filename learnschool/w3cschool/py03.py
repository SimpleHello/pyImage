# -*- coding: utf-8 -*-

"""
一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？
8 输出 9*9 乘法口诀表
"""

def showN(num):
	 num = num +1
	 for i in range(1,num):
	 	for j in range(1,i+1):
	 		print "%d * %d = %d " %(i,j,i*j),
	 	print 

showN(5)