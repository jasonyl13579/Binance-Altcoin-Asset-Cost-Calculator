# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 21:48:28 2021

@author: Corn
"""
from source.assetinfo import save_obj, load_obj
from source.assetinfo import AssetInfo
from source.excelutil import generate_single_report_to_excel
import source.timeutil as tu
class BaseClient:
    def __init__(self, accountname, client_info):
        self.accountname = accountname
        self.assets = load_obj(accountname + '_assets')
        if not self.assets: self.assets = {}
        self.info = client_info
        self.trade_pair_list = []
    def __str__(self):
        return "accountname:" + self.accountname + '\n' + str(self.info)
    def save_assets(self):
        save_obj(self.assets, self.accountname + '_assets')

    def _send_get_request(self, url, with_key = False):
        return NotImplemented
    
    def get_transection_history(self, symbol, starttime):  
        return NotImplemented
    
    def get_current_price(self, symbol):
        return NotImplemented
    
    def get_previous_usdt_price (self, symbol, starttime):
        return NotImplemented
    
    def get_deposite_history(self,starttime, endtime, asset=None ):
        return NotImplemented
    
    def process_transection_history(self, response, trade_pair, asset_obj):
        return NotImplemented
    
    def summary_deposite_history(self):
        return NotImplemented
    
    def persetAsset(assets):
        assets['ETH'].resetAsset(0.14247952, 1600266309450)
        assets['BTC'].resetAsset(0, 1600266309450)
        assets['BNB'].resetAsset(2.95568409, 1600266309450)
    def summary_asset_history(self, updateasset=True):
        print ('Summary account: ' + self.accountname)
        assets = self.assets
        visited_query = set()
        profit = 0
        total_count = 0
        for t in self.trade_pair_list:
             if t not in assets: assets[t] = AssetInfo(t, self.trade_pair_list)
        #if self.accountname == 'binance_Jason': cu.persetAsset(assets)
        for query_asset in self.info.query_list:
            if query_asset not in assets: assets[query_asset] = AssetInfo(query_asset, self.trade_pair_list)
            if updateasset and query_asset not in visited_query:
                visited_query.add(query_asset)
                asset_obj = assets[query_asset]
                asset_obj.current_price = self.get_current_price(query_asset)
                for trade_pair in asset_obj.trade_pair_list:
                    if trade_pair == query_asset: continue
                    symbol = query_asset + trade_pair
                    hasMoreData = True
                    while hasMoreData:
                        response = self.get_transection_history(query_asset , trade_pair, asset_obj.each_last_query_timestamp[trade_pair])
                        count, hasMoreData = self.process_transection_history(response, trade_pair, asset_obj)
                        if count != -1:
                            print ("Add %d %s data." % (count, symbol))
                            total_count += count
                        else:
                            print ("Cant not query symbol: " + symbol)
                            asset_obj.remove_trade_pair(trade_pair)
                profit += (asset_obj.current_price * asset_obj.qty - asset_obj.quoteQty)   
                #asset_obj.print_info()   
        #persetAsset(assets)
        self.info.profit = profit
        self.info.asset_num = len(assets) 
        self.info.last_asset_upgrade_time = tu.get_current_timestamp()
        self.save_assets()
        generate_single_report_to_excel(assets, self.accountname, self.info.save_path)
    
