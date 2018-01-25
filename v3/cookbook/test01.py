from collections import deque

def test02():
    a = {"x": 1, "y": 2, "z": 3}
    b = {"x": 10, "w": 4, "z": 3}
    print(a.items() & b.items())


def test01():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # x1, *x2, x3 = a
    # print(x2)

test01()
