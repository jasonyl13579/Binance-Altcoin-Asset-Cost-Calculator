# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:19:18 2020

@author: Corn
"""

import sys 
from gui import GUI
from clients.clients import Clients

if __name__ == '__main__':

    if len(sys.argv)>1:
        clients = Clients()
        clients.restore_client_config()
        #clients.init_client_from_key("key.txt")
        if sys.argv[1] == "-d":
            clients.start_summary_deposite_history()
        elif sys.argv[1] == "-g":
            clients.start_generate_summary_report_to_excel()
    else:
        window = GUI()
        window.setMainUI()
        window.run()
