# _*_ coding:utf-8 _*_
import time
import test.py01
# 输出 乘法表
def fig(n):
    for i in range(1, n + 1):
        for j in range(1, i + 1):	
            print "%d*%d=%d" % (i, j, i * j),
        print 

# 暂停1秒
def pcs():
    time.sleep(1)
    return "shuchu"


print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print pcs()
print test.py01.meth01();