# -*- coding: utf-8 -*-
"""
Created on Thu May  5 16:48:37 2016

@author: roy
"""

from gevent import monkey; monkey.patch_socket()
import gevent
import requests
import time

t0 = time.time()

def f():
    print("Start Crawling")
    r = requests.get("http://www.baidu.com")
    print("Crawling Finished")
    gevent.sleep(0)
    
gs = []
for _ in range(50):
    g = gevent.spawn(f)
    gs.append(g)

for i in range(50):
    gs[i].join()
    
t1 = time.time()

print(t1-t0)
    



    

