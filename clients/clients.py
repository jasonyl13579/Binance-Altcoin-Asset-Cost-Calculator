# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 23:38:06 2021

@author: Corn
"""
import sys
import traceback
from os import path, getcwd
from json import load, dump

from clients.binance_client import BinanceClient
from clients.ftx_client import FtxClient
from clients.clientinfo import ClientInfo
from source.excelutil import generate_summary_report_to_excel

class Clients:
    def __init__(self, owner=None, meta_save_path=None):
        self.owner = owner
        self.meta_save_path = meta_save_path
        self.count = 0
        self.client_dict = {}
    def add_client(self, name, new_client):
        if name in self.client_dict:
            print ('Client name already exist.')
            return
        else:
            self.client_dict[name] = new_client
    def delete_client(self, name):
        if name not in self.client_dict:
            print ('Client name not exist.')
            return
        else:
            self.count -= 1
            self.client_dict[name].delete_assets()
            del self.client_dict[name]
    def clients_info(self):
        for name, client in self.client_dict.items():
            print (client)
    def start_generate_summary_report_to_excel(self, save_filename = '.config'):
        data, err = None, 0
        for name, client in self.client_dict.items(): 
            err = client.summary_asset_history(updateasset=True)
        if not err: generate_summary_report_to_excel(self.client_dict, self.meta_save_path)
        self.save_client_config(save_filename = save_filename)
        return data
    def start_summary_deposite_history(self, gui = False, save_filename = '.config'):
        res, err = {}, 0
        for name, client in self.client_dict.items():
            (data, err) = client.summary_deposite_history(gui)
            res[name] = data
        if err == NotImplementedError: print(client.info.exchange + " does not support this feature.")
        elif err: print("Error in summary deposite history.")
        self.save_client_config(save_filename = save_filename)
        return res
    def process_summary_deposite_history(self, history, gui, app):
        for name, client in self.client_dict.items():
            client.process_deposite_history(history[client.accountname], gui = True, app=app)
            client.save_assets()
    def process_client_data(self, client_name, client_data):  
        
        client_data['save_path'] = self.meta_save_path
        client_info = ClientInfo()
        client_info.setinfo(client_data)
        if client_data['exchange'] == 'binance':
            new_client = BinanceClient(client_name, client_info)
            self.add_client(client_name, new_client)
        elif client_data['exchange'] in ['ftx', 'ftx_subaccount']:
            new_client = FtxClient(client_name, client_info)
            self.add_client(client_name, new_client)
    def restore_client_config(self, save_filename = '.config'):
        ## https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app 
            # path into variable _MEIPASS'.
            application_path = path.dirname(sys.executable)
        else:
            application_path = getcwd()
        self.meta_save_path = application_path
        #print ("In top:" + self.meta_save_path)
        if not path.isfile(save_filename): 
            self.owner = "name"
            return
        try:
            with open(save_filename, 'r', encoding='utf8') as f:
                config = load(f) 
            if 'meta_save_path' in config: self.meta_save_path = config['meta_save_path']
            self.owner = config['owner']
            self.count = config['count']
            
            for client_name, client_data in config['account'].items():
                #print (client_data)
                self.process_client_data(client_name, client_data)
        except:
            self.owner = "name"
            traceback.print_exc()
            print("Init config fail.")
        print ("In restore:" + self.meta_save_path)
    def save_client_config(self, save_filename = '.config'):
        config = {}
        config['owner'] = self.owner
        config['meta_save_path'] = self.meta_save_path
        config['count'] = self.count
        config['account'] = {}
        for client_name, client in self.client_dict.items():
            client.info.save_path = self.meta_save_path
            config['account'][client_name] = client.info.__dict__
        with open(save_filename, 'w') as f:
            dump(config, f, indent=4)
    def init_client_from_key(self, key_path = None, save_filename = '.config'):
        try:
            if not key_path or not path.isfile(key_path):
                key_path = "source/key_example.txt"
            with open(key_path,'r', encoding="utf-8") as fp:
                data = load(fp)
                if 'meta_save_path' in data: self.meta_save_path = data['meta_save_path']
                if 'owner' in data: self.owner = data['owner']
                
                for client_name, client_data in data['account'].items():
                    if client_name not in self.client_dict:
                        client_data['index'] = self.count
                        self.count += 1
                        self.process_client_data(client_name, client_data)
                    else:
                        self.client_dict[client_name].info.setinfo(client_data)
            self.save_client_config(save_filename)
        except Exception as e:
            print(e)
            print("Init Key fail.")
            
        return 0
