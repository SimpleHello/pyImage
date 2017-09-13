# _*_ coding:utf-8 _*_
import os


def getName(L=[]):
    L.append("end")
    return L


def fname(x):
    return x * x


def fstr(str):
    return str and str.strip()


print map(fname, range(1, 11))
print[d for d in os.listdir('.')]
print int("1234")

str = "123 sds sd qqq   "
print filter(fstr, ['A', '', 'B', None, 'C', '  '])


class Student(object):

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name


bart = Student("张三")

print bart.getName()
