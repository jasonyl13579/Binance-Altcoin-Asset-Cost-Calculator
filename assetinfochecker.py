# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 22:43:29 2021

@author: Corn
"""

from source.assetinfo import AssetInfo, load_obj

accountname = 'binance_Alex'

assets = load_obj(accountname +'_assets')

for name in assets:
    assets[name].print_info()