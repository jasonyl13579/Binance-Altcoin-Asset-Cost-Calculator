# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 23:38:06 2021

@author: Corn
"""
import os
import json
from clients.binance_client import BinanceClient
from clients.ftx_client import FtxClient
import clients.clientsutil as cu
from source.excelutil import generate_summary_report_to_excel
from clients.clientinfo import ClientInfo
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
            self.client_dict[name] = None
    def clients_info(self):
        for name, client in self.client_dict.items():
            print (client)
    def start(self, cal_deposite = False):
        for name, client in self.client_dict.items(): 
            if cal_deposite:
                client.summary_deposite_history()
            else:
                client.summary_asset_history(updateasset=True)
        self.save_client_config()
        generate_summary_report_to_excel(self.client_dict, self.meta_save_path)
    def process_client_data(self, client_name, client_data):        
        client_info = ClientInfo()
        client_info.setinfo(client_data)
        if client_data['exchange'] == 'binance':
            new_client = BinanceClient(client_name, client_info)
            self.add_client(client_name, new_client)
        elif client_data['exchange'] == 'ftx':
            new_client = FtxClient(client_name, client_info)
            self.add_client(client_name, new_client)
    def restore_client_config(self):
        if not os.path.isfile('config.json'): return
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            meta_save_path = './'
            if 'meta_save_path' in config: meta_save_path = config['meta_save_path']
            self.owner = config['owner']
            self.meta_save_path = config['meta_save_path']
            self.count = config['count']
            for client_name, client_data in config['account'].items():
                self.process_client_data(client_name, client_data)
        except:
            print("Init config fail.")
    def save_client_config(self):
        config = {}
        config['owner'] = self.owner
        config['meta_save_path'] = self.meta_save_path
        config['count'] = self.count
        config['account'] = {}
        for client_name, client in self.client_dict.items():
            config['account'][client_name] = client.info.__dict__
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
def init_client_from_key(key_path = None):
    try:
        clients = Clients()
        clients.restore_client_config()
        if not key_path or not os.path.isfile(key_path):
            key_path = "source/key_example.txt"
        with open(key_path,'r', encoding="utf-8") as fp:
            data = json.load(fp)
            meta_save_path = './'
            if 'meta_save_path' in data: meta_save_path = data['meta_save_path']
            if not clients.owner:
                clients.owner, clients.meta_save_path = data['owner'], meta_save_path
            for client_name, client_data in data['account'].items():
                if client_name not in clients.client_dict:
                    client_data['index'] = clients.count
                    clients.process_client_data(client_name, client_data)
                    clients.count += 1
                else:
                    clients.client_dict[client_name].info.setinfo(client_data)
    except Exception as e:
        print(e)
        print("Init Key fail.")
        
    return clients
