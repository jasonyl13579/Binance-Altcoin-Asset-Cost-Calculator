# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 15:53:19 2020

@author: Corn
"""
from datetime import datetime
from source.timeutil import get_current_timestamp, phrase_iso_to_time, datetime_to_utc_time
from pickle import load, dump, HIGHEST_PROTOCOL
from os import path, remove, mkdir


class AssetInfo():
    def __init__(self, name = None, trade_pair_list = None, qty = 0.0, last_query_timestamp = None):
        self.name = name
        self.cost = 0.00000
        self.qty = qty
        self.quoteQty = 0.0
        self.current_price = 0.0
        self.transection_count = 0
        self.deposit_count = 0
        self.last_query_timestamp = last_query_timestamp
        self.each_last_query_timestamp = {}
        self.trade_pair_list = trade_pair_list.copy()
        for t in self.trade_pair_list:
            self.each_last_query_timestamp[t] = None
    
    
    def resetAsset(self,qty , last_query_timestamp):
        self.cost = 0.00000
        self.qty = qty
        self.quoteQty = qty * self.current_price
        self.transection_count = 0
        self.deposit_count = 0
        self.last_query_timestamp = last_query_timestamp
        for t in self.trade_pair_list:
            self.each_last_query_timestamp[t] = last_query_timestamp
    def upgrade_time(self, tradepair, time):
        ## add 1 second to avoid duplication
        if not self.each_last_query_timestamp[tradepair] or self.each_last_query_timestamp[tradepair] < float(time): 
            self.each_last_query_timestamp[tradepair] = float(time+1001)
        if not self.last_query_timestamp or self.last_query_timestamp < float(time): 
            self.last_query_timestamp = float(time+1001)
    def _upgrade(self, qty, quoteQty, isBuyer=True):
        if isBuyer:
            self.qty += qty
            self.quoteQty += quoteQty
        else:
            self.qty -= qty
            self.quoteQty -= quoteQty
        if self.qty <= 0.00001: 
            self.cost = 0
        else: 
            self.cost = (self.quoteQty) / (self.qty) 
    def upgrade_by_deposit(self, qty, quoteQty, isBuyer=True):
        self._upgrade(qty, quoteQty, isBuyer)
        self.deposit_count += 1
    def upgrade_by_transection(self, transection):
        self._upgrade(transection['qty'], transection['quoteQty'], transection['isBuyer'])
        self.transection_count += 1
        self.upgrade_time('USDT', transection['time'])
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
        self.upgrade_time(trade_pair, transection['time'])
    def pay_commission(self, number):
        self.qty -= number
    def remove_trade_pair(self, trade_pair):
        if trade_pair in self.trade_pair_list: self.trade_pair_list.remove(trade_pair)
                
    def print_info(self):
        print ("Asset name: %s" % self.name)
        print ("Quantity: %f" % self.qty)
        print ("Average per cost: %f" % self.cost)
        print ("Current price: %f\n" % self.current_price)
        
        print ("USDT total cost: %f" % self.quoteQty)
        print ("Current USDT value: %f" % (self.current_price * self.qty))
        print ("Current profit: %f\n" % (self.current_price * self.qty - self.quoteQty))
        
        print ("Transection count: %d" % self.transection_count)
        if self.last_query_timestamp:
            print ("Last transection time: %s" % datetime_to_utc_time(self.last_query_timestamp)) 
        else:
            print ("Last transection time: No history.")
        print (self.trade_pair_list)
        for t in self.trade_pair_list:
            print ("%s:%s" % (t, datetime_to_utc_time(self.each_last_query_timestamp[t])))
        print ("-----------------------------------------")\


def save_obj(obj, name ):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            dump(obj, f, HIGHEST_PROTOCOL)
def load_obj(name) -> dict:
    try:
        if not path.exists('obj/'): mkdir('obj/')
        with open('obj/' + name + '.pkl', 'rb') as f:
            obj =  load(f)
            return obj
        
    except:
        return None
def delete_obj(name):
    try:
        remove('obj/' + name + '.pkl')
    except:
        print ("Delete fail.")