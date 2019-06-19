import threadpool
import time


def Main_Def(par1, par2, par3):
    print "par1 = %s, par2 = %s, par3 = %s" % (par1, par2, par3)


if __name__ == '__main__':
    list_var1 = ['1', '2', '3']
    list_var2 = ['4', '5', '6']
    par_list = [(list_var1, None)]
    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(Main_Def, par_list)
    [pool.putRequest(req) for req in requests]
    time.sleep(1)
    pool.wait()