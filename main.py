# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:19:18 2020

@author: Corn
"""
import requests
import time
import os
import json
import pickle
from source.apisignature import create_signature_with_query
from source.assetinfo import AssetInfo
from source.excelutil import save_to_excel

query_list = ['BTS', 'BTC', 'ETH', 'ALGO', 'SRM', 'XRP', 'IOTA', \
              'NULS', 'SXP', 'SOL', 'XTZ', 'SUSHI', 'TRX', 'DOT','LINK','BNB', \
              'BCH', 'EOS', 'XLM', 'ATOM']
    
trade_pair_list = ['USDT','BTC','ETH','BNB']

#query_list = ['BTSUSDT','BTCUSDT']
#last_query_timestamp = json.load( open("file_name.json"))
try:
    key_path = "key.txt"
    if not os.path.isfile(key_path):
        key_path = "source/key_example.txt"
    with open(key_path,'r', encoding="utf-8") as fp:
        data = json.load(fp)
        if 'api_key' not in data:
            raise ('api_key not exist')
        if 'secret_key' not in data:
            raise ('secret_key not exist')
        if 'save_path' in data:
            save_path = data['save_path']
        else: save_path = './'
        api_key = data['api_key']
        secret_key = data['secret_key']
except:
    raise
def persetAsset(assets):
    assets['ETH'].resetAsset(0.14247952, 1600266309450)
    assets['BTC'].resetAsset(0, 1600266309450)
    assets['BNB'].resetAsset(2.95568409, 1600266309450)
def get_current_timestamp():
    return int(round(time.time() * 1000))

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    try:
        if not os.path.exists('obj/'): os.mkdir('obj/')
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {}
def get_transection_history(symbol, starttime):    
    query =  "symbol=%s&limit=500&timestamp=%d" % (symbol, get_current_timestamp())
    if starttime: query += "&%d" % starttime
    signature = create_signature_with_query(secret_key, query)   
    url = "https://api.binance.com/api/v3/myTrades?%s&signature=%s"  % (query, signature)
    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'X-MBX-APIKEY': api_key
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    return response
def get_current_price(symbol):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=%s" % symbol
    payload = {}
    headers = {
      'Content-Type': 'application/json'
    }    
    response = requests.request("GET", url, headers=headers, data = payload) 
    if 'price' not in response.json():
        print ('Cant find %s price.' % symbol)
        return -1
    else: return float(response.json()['price'])
    #print(response.text.encode('utf8'))
def get_previous_usdt_price (symbol, starttime):
    url = "https://api.binance.com/api/v3/klines?symbol=%sUSDT&interval=1m&startTime=%d&limit=1" % (symbol, starttime)
    payload = {}
    headers = {
      'Content-Type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    #print (response.text)
   # print ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
    return ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
if __name__ == '__main__':
    assets = load_obj('assets')
    for t in trade_pair_list:
        if t not in assets: assets[t] = AssetInfo(t)
    for query_asset in query_list:
        if query_asset not in assets: assets[query_asset] = AssetInfo(query_asset)
        asset_obj = assets[query_asset]
        asset_obj.current_price = get_current_price(query_asset + 'USDT')
        
        for trade_pair in trade_pair_list:
            if trade_pair == query_asset: continue
            symbol = query_asset + trade_pair
            response = get_transection_history(symbol, asset_obj.each_last_query_timestamp[trade_pair])
            if response:
                
                for transection in response.json():
                    if trade_pair == 'USDT': 
                        #asset_obj.upgrade(transection)
                        asset_obj.upgrade_by_other_pair(transection, assets[trade_pair], 1)
                    else:
                        #query_asset_price = get_previous_usdt_price (query_asset, transection['time'])
                        trade_pair_price = get_previous_usdt_price (trade_pair, transection['time'])
                        asset_obj.upgrade_by_other_pair(transection, assets[trade_pair], trade_pair_price)
                    assets[transection['commissionAsset']].pay_commission(float(transection['commission']))
                    
                print ("Add %d %s data." % (len(response.json()), symbol))
        asset_obj.print_info()   
    #persetAsset(assets)
    save_obj(assets, 'assets')
    save_to_excel('assets', save_path)
#print(response.text.encode('utf8'))
