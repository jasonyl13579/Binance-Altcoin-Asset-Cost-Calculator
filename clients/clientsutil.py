# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:20:40 2021

@author: Corn
"""

from source.assetinfo import AssetInfo
from source.excelutil import generate_single_report_to_excel
from source.timeutil import *
#query_list = ['ALGO']
trade_pair_list = ['USDT','BTC','ETH','BNB']


        
def persetAsset(assets):
    
    assets['ETH'].resetAsset(0.14247952, 1600266309450)
    assets['BTC'].resetAsset(0, 1600266309450)
    assets['BNB'].resetAsset(2.95568409, 1600266309450)

