# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 01:01:26 2021

@author: Corn
"""
import source.timeutil as tu

class ClientInfo():
    def __init__(self, api_key=None, api_secret=None, accountname=None, save_path='./', query_list=None, index=0, timestamp=tu.DEFAULT_EPOCH_TIME):
        self.api_key = api_key
        self.api_secret = api_secret
        self.save_path = save_path
        self.query_list = query_list
        self.exchange = 'default'
        self.profit = 0
        self.asset_num = 0
        self.index = index
        self.deposit_USDT = 0
        self.last_asset_upgrade_time = tu.DEFAULT_EPOCH_TIME
        self.last_deposit_timestamp = timestamp 
    def __str__(self):
        return "利潤: %s\n 資產數量: %s\n 存入 USDT: %s \n 資產更新時間: %s\n" \
    % (self.profit, self.asset_num, self.deposit_USDT, tu.datetime_to_utc_time(self.last_asset_upgrade_time))
    def setinfo(self, data):
        try:
            if 'api_key' not in data:
                raise ('api_key not exist')
            if 'api_secret' not in data:
                raise ('api_secret not exist')
            self.api_key = data['api_key']
            self.api_secret = data['api_secret']
            if 'save_path' in data: self.save_path = data['save_path']
            if 'query_list' in data: self.query_list = data['query_list']
            if 'exchange' in data: self.exchange = data['exchange']
            if 'profit' in data: self.profit = data['profit']
            if 'asset_num' in data: self.asset_num = data['asset_num']
            if 'index' in data: self.index = data['index']
            if 'deposit_USDT' in data: self.deposit_USDT = data['deposit_USDT']
            if 'last_asset_upgrade_time' in data: self.last_asset_upgrade_time = data['last_asset_upgrade_time']
            if 'last_deposit_timestamp' in data: self.last_deposit_timestamp = data['last_deposit_timestamp']
            
        except Exception as e:
            print(str(e) + "not exist.")
            print("Set info fail.")
            