# -*- coding: utf8 -*-
__author__ = 'zhaofucheng'
from catchImg import getImg
from catchMP3 import getMp3

import threading

if __name__ == '__main__':
    print '开始抓取......'
    t1 = threading.Thread(target=getImg, name='LoopThread1')
    t2 = threading.Thread(target=getMp3, name='LoopThread2')

    t1.start()
    t2.start()

    t1.join()
    t2.join()