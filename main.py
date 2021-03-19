# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:19:18 2020

@author: Corn
"""

import sys 
from clients.clients import init_client_from_key 


if __name__ == '__main__':
    
    clients = init_client_from_key("key.txt")
    if len(sys.argv)>1 and sys.argv[1] == "-d":
        clients.start(cal_deposite = True)
    else:
        clients.start()
