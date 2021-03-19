# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 23:37:28 2021

@author: Corn
"""
import requests


from source.assetinfo import AssetInfo, save_obj, load_obj
from source.apisignature import create_signature_with_query
from source.timeutil import get_current_timestamp
from clients.clientinfo import ClientInfo
_binanceUrl = 'https://api.binance.com/'
 
class BinanceClient:
   
    def __init__(self, accountname, client_info):
        self.accountname = accountname
        self.assets = load_obj(accountname + '_assets')
        if not self.assets: self.assets = {}
        client_info.exchange = 'binance'
        self.info = client_info
    def __str__(self):
        return "accountname:" + self.accountname + '\n' + str(self.info)
    def save_assets(self):
        save_obj(self.assets, self.accountname + '_assets')

    def _send_get_request(self, url, with_key = False):
        payload = {}
        headers = {
          'Content-Type': 'application/json',
        }
        if with_key: headers['X-MBX-APIKEY'] = self.info.api_key
        return requests.request("GET", url, headers=headers, data = payload)
    def get_transection_history(self, symbol, starttime):  
        #print (symbol, starttime)
        query =  "symbol=%s&limit=500&timestamp=%d" % (symbol, get_current_timestamp())
        if starttime: query += "&startTime=%d" % starttime
        signature = create_signature_with_query(self.info.api_secret, query)   
        #print (query)
        url = _binanceUrl + "api/v3/myTrades?%s&signature=%s"  % (query, signature)
        
        return self._send_get_request(url, with_key=True)
    def get_current_price(self, symbol):
        url = _binanceUrl + "api/v3/ticker/price?symbol=%s" % symbol
        response = self._send_get_request(url)
        
        if 'price' not in response.json():
            print ('Cant find %s price.' % symbol)
            return -1
        else: return float(response.json()['price'])
    def get_previous_usdt_price (self, symbol, starttime):
        url = _binanceUrl + "api/v3/klines?symbol=%sUSDT&interval=1m&startTime=%d&limit=1" % (symbol, starttime)

        response = self._send_get_request(url)
        #print (response.text)
        #print ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
        return ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
    
    def get_deposite_history(self,starttime, endtime, asset=None ):
        query =  "startTime=%d&endTime=%d&timestamp=%d" % (starttime, endtime, get_current_timestamp())
        if asset: query += "&asset=%s" % (asset)
        signature = create_signature_with_query(self.info.api_secret, query)   
        url = _binanceUrl + "wapi/v3/depositHistory.html?%s&signature=%s"  % (query, signature)
        
        return self._send_get_request(url, with_key=True)