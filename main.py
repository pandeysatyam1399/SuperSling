# from subprocess import call
import multiprocessing as mp
from threading import Thread
import os
import superSling
# import itachIP2IR
import keyPress

res = mp.Value('i')

def keyListen(res):
    # print(type(res))
    print('parent process ',os.getppid())
    print('process id ',os.getpid())
    # p3 = mp.Process(target=listenKey,args=(res,))
    # p3.start()
    # p3.join()
    keyPress.runner()
    # call(["python","{}".format('keyPress.py')])

def sling(res):
    # res.value = 15
    print('parent process ',os.getppid())
    print('process id ',os.getpid())
    superSling.superRunner(res)
    # call(["python","{}".format('superSling.py')])

# def listenKey(res):
#     keyPress.onPress(res)
# start the key listener when single view
if __name__ == '__main__':
    p2 = mp.Process(target=sling, args=(res,))
    p2.start()
    p1 = mp.Process(target=keyListen,args=(res,))
    p1.start()
    # p3 = mp.Process(target=listenKey,args=(res,))
    # p3.start()
    p2.join()
    p1.join()
    # p3.join()