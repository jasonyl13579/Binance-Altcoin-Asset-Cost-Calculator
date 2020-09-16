# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 15:53:19 2020

@author: Corn
"""
from datetime import datetime



trade_pair_list = ['USDT','BTC','ETH','BNB']

class AssetInfo():
    def __init__(self, name = None, qty = 0.0, last_query_timestamp = None):
        self.name = name
        self.cost = 0.00000
        self.qty = qty
        self.quoteQty = 0.0
        self.current_price = 0.0
        self.transection_count = 0
        self.last_query_timestamp = last_query_timestamp
        self.each_last_query_timestamp = {}
        for t in trade_pair_list:
            self.each_last_query_timestamp[t] = last_query_timestamp
    def resetAsset(self,qty , last_query_timestamp):
        self.cost = 0.00000
        self.qty = qty
        self.quoteQty = qty * self.current_price
        self.transection_count = 0
        self.last_query_timestamp = last_query_timestamp
        for t in trade_pair_list:
            self.each_last_query_timestamp[t] = last_query_timestamp
    def upgrade(self, transection):
        if transection['isBuyer']:
            self.qty += float(transection['qty'])
            self.quoteQty += float(transection['quoteQty'])
        else:
            self.qty -= float(transection['qty'])
            self.quoteQty -= float(transection['quoteQty'])
            
        if self.qty <= 0.00001: 
            self.cost = 0
        else: 
            self.cost = (self.quoteQty) / (self.qty) 
            
        self.transection_count += 1
        if not self.each_last_query_timestamp['USDT'] or self.each_last_query_timestamp['USDT'] < float(transection['time']): self.each_last_query_timestamp['USDT'] = float(transection['time']+1)
        if not self.last_query_timestamp or self.last_query_timestamp < float(transection['time']): self.last_query_timestamp = float(transection['time']+1)
    def upgrade_by_other_pair(self, transection, asset_trade_pair, trade_pair_price):
        trade_pair = asset_trade_pair.name
        if transection['isBuyer']:
            self.qty += float(transection['qty'])
            self.quoteQty += (float(transection['quoteQty']) * trade_pair_price)
            asset_trade_pair.qty -= float(transection['quoteQty'])
            asset_trade_pair.quoteQty -= (float(transection['quoteQty']) * trade_pair_price)
        else:
            self.qty -= float(transection['qty'])
            self.quoteQty -= (float(transection['quoteQty']) * trade_pair_price)
            asset_trade_pair.qty += float(transection['quoteQty'])
            asset_trade_pair.quoteQty += (float(transection['quoteQty']) * trade_pair_price)
        
        if self.qty <= 0.00001: 
            self.cost = 0
        else: 
            self.cost = (self.quoteQty) / (self.qty) 
        if asset_trade_pair.qty <= 0.0001: 
            asset_trade_pair.cost = 0
        else: 
            asset_trade_pair.cost = (asset_trade_pair.quoteQty) / (asset_trade_pair.qty)
        self.transection_count += 1
        if not self.each_last_query_timestamp[trade_pair] or self.each_last_query_timestamp[trade_pair] < float(transection['time']): self.each_last_query_timestamp[trade_pair] = float(transection['time']+1)
        if not self.last_query_timestamp or self.last_query_timestamp < float(transection['time']): self.last_query_timestamp = float(transection['time']+1)
    def pay_commission(self, number):
        self.qty -= number
    def print_info(self):
        print ("Asset name: %s" % self.name)
        print ("Quantity: %f" % self.qty)
        print ("Average per cost: %f" % self.cost)
        print ("Current price: %f\n" % self.current_price)
        
        print ("USDT total cost: %f" % self.quoteQty)
        print ("Current USDT value: %f" % (self.current_price * self.qty))
        print ("Current profit: %f\n" % (self.current_price * self.qty - self.quoteQty))
        
        print ("Transection count: %d" % self.transection_count)
        print ("Last transection time: %s" % datetime.utcfromtimestamp(float(self.last_query_timestamp/1000))) 
        print ("-----------------------------------------")