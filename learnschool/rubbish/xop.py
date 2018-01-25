# _*_ coding:utf-8 _*_

def met():
    x = 0
    for i in range(1, 10):
        for j in range(0, 10):
            for z in range(0, 10):
                if i == j or j == z or i == z:
                    if i == j and i == z:
                        pass
                    else:
                        print "met1 this :", i, j, z
                        x += 1
    return x

def met2():
    x = 0
    for a in range(100,1000):
        i = a/100
        j = a/10%10
        z = a%10
        if i == j or j == z or i == z:
            if i == j and i == z:
                pass
            else:
                print "met2 this :", i, j, z
                x += 1
    return x

print met2()
