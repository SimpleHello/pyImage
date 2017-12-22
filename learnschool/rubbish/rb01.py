# -*- coding=utf-8 -*-
import random


def getByte(num):
    dc = []
    for i in range(1, num + 1):
        dc.append(random.randint(10, 20))
    return dc


a = [1, 2, 3]
b = [3, 4, 2]
print a
