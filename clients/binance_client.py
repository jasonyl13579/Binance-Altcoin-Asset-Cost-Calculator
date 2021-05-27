# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 23:37:28 2021

@author: Corn
"""
from requests import request

from source.assetinfo import AssetInfo
from source.apisignature import create_signature_with_query
import source.timeutil as tu
from source.guiutil import inputDialog
from clients.base_client import BaseClient
class BinanceClient(BaseClient):
   
    def __init__(self, accountname, client_info):
        super().__init__(accountname, client_info)
        self.trade_pair_list = ['USDT','BTC','ETH','BNB']
        self.info.exchange = 'binance'
        self._domain_url = 'https://api.binance.com/'
    def _send_get_request(self, url, with_key = False):
        payload = {}
        headers = {
          'Content-Type': 'application/json',
        }
        if with_key: headers['X-MBX-APIKEY'] = self.info.api_key
        return request("GET", url, headers=headers, data = payload)
    def check_account_status(self):
        response = self.get_transection_history('BTC', 'USDT', tu.get_current_timestamp()-10000000)
        #print(tu.datetime_to_utc_time(tu.get_current_timestamp()-10000000))
        if response.status_code != 200:
            if response.status_code == 401:
                print (response.json()['msg'])
                print ('Your api_key: ' + self.info.api_key)
            elif response.status_code == 400:
                print (response.json())
                print ('Invaild api_key or secret key.')
            else:
                print ('Cant connect server.')
            return 1
        return 0
        
    def get_transection_history(self, query_asset , trade_pair, starttime):  
        symbol = query_asset + trade_pair
        #print (symbol, starttime)
        query =  "symbol=%s&limit=500&timestamp=%d" % (symbol, tu.get_current_timestamp())
        if starttime: query += "&startTime=%d" % starttime
        signature = create_signature_with_query(self.info.api_secret, query)   
        #print (query)
        url = self._domain_url + "api/v3/myTrades?%s&signature=%s"  % (query, signature)
        return self._send_get_request(url, with_key=True)
    def get_current_price(self, symbol):
        url = self._domain_url + "api/v3/ticker/price?symbol=%s" % (symbol + 'USDT')
        response = self._send_get_request(url)
        
        if 'price' not in response.json():
            print ('Cant find %s price.' % symbol)
            return -1
        else: return float(response.json()['price'])
    def get_previous_usdt_price (self, symbol, starttime):
        url = self._domain_url + "api/v3/klines?symbol=%sUSDT&interval=1m&startTime=%d&limit=1" % (symbol, starttime)

        response = self._send_get_request(url)
        #print ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
        return ((float(response.json()[0][2]) + float(response.json()[0][3])) / 2)
    
    def get_deposite_history(self,starttime, endtime, asset=None ):
        query =  "startTime=%d&endTime=%d&timestamp=%d" % (starttime, endtime, tu.get_current_timestamp())
        if asset: query += "&asset=%s" % (asset)
        signature = create_signature_with_query(self.info.api_secret, query)   
        url = self._domain_url + "wapi/v3/depositHistory.html?%s&signature=%s"  % (query, signature)
        
        return self._send_get_request(url, with_key=True)
    def process_transection_history(self, response, trade_pair, asset_obj):
        count = 0
        if response and response.status_code == 200:
            for transection in response.json():
                count += 1
                #print (transection)
                if trade_pair == 'USDT': 
                    #asset_obj.upgrade(transection)
                    asset_obj.upgrade_by_other_pair(transection, self.assets[trade_pair], 1)
                else:
                    trade_pair_price = self.get_previous_usdt_price (trade_pair, transection['time'])
                    asset_obj.upgrade_by_other_pair(transection, self.assets[trade_pair], trade_pair_price)
                self.assets[transection['commissionAsset']].pay_commission(float(transection['commission']))
                #asset_obj.print_info()
            return (count, False)
        else:
            return (-1, False)
    def summary_deposite_history(self, gui = False):
        INIT_EPOCH = 1483228800000 # 2017/01/01
        EPOCH_INTERVAL= 5000000000
        epoch = INIT_EPOCH if not self.info.last_deposit_timestamp else self.info.last_deposit_timestamp
        assets = self.assets
        data = []
        print (self.accountname)
        while epoch < tu.get_current_timestamp():
            res = self.get_deposite_history(epoch, epoch + EPOCH_INTERVAL)
            print ("Processing " + (tu.datetime_to_utc_time(epoch)) + " to " + tu.datetime_to_utc_time(epoch + EPOCH_INTERVAL))
            if res.json()["depositList"]:
                if gui:
                    data.append((self.accountname, res.json()["depositList"]))
                else:
                    self.process_deposite_history(res.json()["depositList"])
                    #print (tu.datetime_to_utc_time(self.info.last_deposit_timestamp))
                
            epoch += EPOCH_INTERVAL
        
        self.save_assets()
        return (data, 0)
    def process_deposite_history(self, history, gui = False, app=None):
        ## GUI only work in main thread
        assets = self.assets
        for (accountname, depositList) in history:
            for deposit in sorted(depositList, key=lambda x:x['insertTime']):
                query_asset = deposit['asset']
                if query_asset not in assets: assets[query_asset] = AssetInfo(query_asset, self.trade_pair_list)
                asset_obj = assets[query_asset]
                if deposit['asset'] != "USDT":
                    question = "帳戶:%s\n輸入本%s紀錄的USDT成本. \n(數量:%f, 時間:%s):" % \
                        (accountname, deposit['asset'], deposit['amount'],tu.datetime_to_utc_time(deposit['insertTime']))
                    if gui:
                        if app == None: return 
                        
                        dialog = inputDialog(app, question)
                        app.wait_window(dialog)
                        cost = float(dialog.output)
                    else:
                        cost = float(input(question))
                    asset_obj.upgrade_by_deposit(deposit['amount'], cost*deposit['amount'])
                    asset_obj.print_info()
                else:
                    self.info.deposit_USDT = self.info.deposit_USDT + deposit['amount']
                if not self.info.last_deposit_timestamp or self.info.last_deposit_timestamp < deposit['insertTime']:
                    self.info.last_deposit_timestamp = deposit['insertTime'] + 1