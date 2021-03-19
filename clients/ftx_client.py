# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 23:37:28 2021

@author: Corn
"""
import requests


from source.assetinfo import AssetInfo, save_obj, load_obj
from source.apisignature import create_signature_with_query
from source.timeutil import get_current_timestamp, phrase_iso_to_time
from clients.base_client import BaseClient
from source.excelutil import generate_single_report_to_excel

class FtxClient(BaseClient):
   
    def __init__(self, accountname, client_info):
        super().__init__(accountname, client_info)
        self.trade_pair_list = ['USD','USDT']
        self.info.exchange = 'ftx'
        self._domain_url = 'https://ftx.com/api/'
        
    def _send_get_request(self, query):
        payload = {}
        time = str(get_current_timestamp())
        method = 'GET/api/'
        signature_payload = '%s%s%s' % (time, method, query) 
        headers = {
          'Content-Type': 'application/json',
          'FTX-KEY': self.info.api_key,
          'FTX-SIGN': create_signature_with_query(self.info.api_secret, signature_payload),
          'FTX-TS': time
        }
        url = self._domain_url + query
        return requests.request("GET", url, headers=headers, data = payload)
    def get_transection_history(self, query_asset , trade_pair, starttime=None):  
        #print (symbol, starttime)
        query =  "orders/history?market=%s" % (query_asset + '/' + trade_pair)
        if starttime: query += "&start_time=%d" % starttime
        return self._send_get_request(query)
    def get_current_price(self, symbol):
        query =  "markets/%s" % (symbol + '/USDT')
        response = self._send_get_request(query)
        
        if response.json()['success'] != True:
            print ('Cant find %s price.' % symbol)
            return -1
        else: return float(response.json()['result']['price'])
    def get_previous_usdt_price (self, query_asset, end_time):
        ##　GET /markets/{market_name}/candles?resolution={resolution}&limit={limit}&start_time={start_time}&end_time={end_time}
        query =  "/markets/%s/candles?limit=1&resolution=15&end_time=%s" % (query_asset + '/USDT', str(end_time) )
        response = self._send_get_request(query)
        #print (response.json())
        return response.json()['result'][0]['close']
    
    def get_deposite_history(self,starttime=None, endtime=None, asset=None ):
        query = 'wallet/deposits'
        if starttime: query += "&start_time=%d" % starttime
        if endtime: query += "&end_time=%d" % endtime
        return self._send_get_request(query)
    
    # def summary_asset_history(self, updateasset=True):
    #     assets = self.assets
    #     visited_query = set()
    #     profit = 0
    #     for t in self.trade_pair_list:
    #          if t not in assets: assets[t] = AssetInfo(t, self.trade_pair_list)
    #     for query_asset in self.info.query_list:
    #         if query_asset not in assets: assets[query_asset] = AssetInfo(query_asset, self.trade_pair_list)
    #         if updateasset and query_asset not in visited_query:
    #             visited_query.add(query_asset)
    #             asset_obj = assets[query_asset]
    #             asset_obj.current_price = self.get_current_price(query_asset)
    #             for trade_pair in self.trade_pair_list:
    #                 if trade_pair == query_asset: continue
    #                 symbol = query_asset + trade_pair
    #                 response = self.get_transection_history(query_asset , trade_pair, asset_obj.each_last_query_timestamp[trade_pair])
    #                 if not self.process_transection_history(response, trade_pair, asset_obj):
    #                     print ("Add %d %s data." % (len(response.json()), symbol))
    #                 else:
    #                     print ("Cant not query symbol: " + symbol)
    #             profit += (asset_obj.current_price * asset_obj.qty - asset_obj.quoteQty)   
    #             #print (asset_obj.current_price * asset_obj.qty - asset_obj.quoteQty)
    #             #asset_obj.print_info()   
    #     #persetAsset(assets)
    #     self.info.profit = profit
    #     self.info.asset_num = len(assets)
    #     self.info.last_asset_upgrade_time = get_current_timestamp()
    #     self.save_assets()
    #     generate_single_report_to_excel(assets, self.accountname, self.info.save_path)
    def process_transection_history(self, response, trade_pair, asset_obj):
        count = 0
        if response and response.status_code == 200:    
            for result in response.json()['result']:
                asset_obj.upgrade_time(trade_pair, phrase_iso_to_time(result['createdAt']))
                if result['filledSize'] == 0 or ( not result['avgFillPrice'] and not result['price']): continue
                price = result['avgFillPrice'] if result['avgFillPrice'] else result['price']
                transection = { 'time': phrase_iso_to_time(result['createdAt']),
                      'isBuyer': True if result['side'] == 'buy' else False,
                      'qty': result['filledSize'],
                      'quoteQty': result['filledSize'] * price
                    }
                if trade_pair == 'USDT' or trade_pair == 'USD': 
                    #asset_obj.upgrade(transection)
                    asset_obj.upgrade_by_other_pair(transection, self.assets[trade_pair], 1)
                else:
                    #query_asset_price = get_previous_usdt_price (query_asset, transection['time'])
                    trade_pair_price = self.get_previous_usdt_price (trade_pair, transection['time']/1000)
                    asset_obj.upgrade_by_other_pair(transection, self.assets[trade_pair], trade_pair_price)
                #self.assets[transection['commissionAsset']].pay_commission(float(transection['commission']))
                count += 1
            return (count, response.json()['hasMoreData'])
        else:
            return (-1, False)